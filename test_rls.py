import requests
import uuid
import sys

BASE_URL = "http://localhost:5000/api"

def create_tenant(name):
    resp = requests.post(f"{BASE_URL}/tenants/", json={"name": name})
    if resp.status_code == 201:
        return resp.json()
    print(f"Failed to create tenant {name}: {resp.text}")
    print("If 500 error, ensure DB is running and init_db.sql was executed.")
    sys.exit(1)

def create_project(tenant_id, name):
    headers = {"X-Tenant-ID": tenant_id}
    resp = requests.post(f"{BASE_URL}/projects/", json={"name": name, "description": f"Project for {tenant_id}"}, headers=headers)
    if resp.status_code == 201:
        print(f"Created project '{name}' for tenant {tenant_id}")
        return resp.json()
    print(f"Failed to create project for {tenant_id}: {resp.status_code} {resp.text}")
    return None

def list_projects(tenant_id):
    headers = {"X-Tenant-ID": tenant_id}
    resp = requests.get(f"{BASE_URL}/projects/", headers=headers)
    if resp.status_code == 200:
        return resp.json()
    print(f"Failed to list projects for {tenant_id}: {resp.status_code} {resp.text}")
    return []

def main():
    print("--- 1. Creating Tenants ---")
    tenant_a = create_tenant("Acme Corp")
    tenant_b = create_tenant("Beta Inc")
    
    id_a = tenant_a['id']
    id_b = tenant_b['id']
    
    print(f"Tenant A: {id_a}")
    print(f"Tenant B: {id_b}")
    
    print("\n--- 2. Creating Projects ---")
    create_project(id_a, "Project Alpha (A)")
    create_project(id_a, "Project Apollo (A)")
    create_project(id_b, "Project Beta (B)")
    
    print("\n--- 3. Verifying Isolation ---")
    
    print(f"Querying as Tenant A ({id_a})...")
    projects_a = list_projects(id_a)
    print(f"Found {len(projects_a)} projects.")
    for p in projects_a:
        print(f" - {p['name']} (Tenant: {p['tenant_id']})")
        if p['tenant_id'] != id_a:
            print("!!! ERROR: LEAK DETECTED! Found project from another tenant!")
    
    print(f"\nQuerying as Tenant B ({id_b})...")
    projects_b = list_projects(id_b)
    print(f"Found {len(projects_b)} projects.")
    for p in projects_b:
        print(f" - {p['name']} (Tenant: {p['tenant_id']})")
        if p['tenant_id'] != id_b:
            print("!!! ERROR: LEAK DETECTED! Found project from another tenant!")
            
    if len(projects_a) == 2 and len(projects_b) == 1:
        print("\n--- SUCCESS: Strict Tenant Isolation Verified! ---")
    else:
        print("\n--- FAILURE: Counts do not match expected values. ---")

if __name__ == "__main__":
    main()
