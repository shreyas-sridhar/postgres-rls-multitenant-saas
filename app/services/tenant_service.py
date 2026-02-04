from app.models import Tenant
from app.db import db

class TenantService:
    @staticmethod
    def create_tenant(name):
        import uuid
        from app.db import set_tenant_context
        
        # Explicitly generate ID so we can set RLS context BEFORE insertion
        new_tenant_id = str(uuid.uuid4())
        print(f"DEBUG: Generated UUID: {new_tenant_id} (type: {type(new_tenant_id)})")
        
        try:
            # Set context to allow this insertion (RLS Policy: id = current_tenant)
            print("DEBUG: Setting context...")
            set_tenant_context(new_tenant_id)
            
            print("DEBUG: Context set. Creating model...")
            # pg8000 might prefer UUID object for UUID column
            tenant = Tenant(id=uuid.UUID(new_tenant_id), name=name)
            db.session.add(tenant)
            
            # Serialize before commit to avoid refresh triggering RLS without context
            result_data = {
                'id': str(tenant.id),
                'name': tenant.name,
                'created_at': None # Approximating or we can fetch time
            }
            
            print("DEBUG: Committing...")
            db.session.commit()
            print("DEBUG: Commit success.")
            
            # Create a dummy object or return dict? 
            # The service returns 'tenant' object usually.
            # But the route calls .to_dict().
            # Let's attach to_dict to this instance so it returns cached data?
            # Or better: make service return dict or logic.
            # Simplest for now: ensure to_dict() works.
            tenant.to_dict = lambda: result_data
            
            return tenant
        except Exception as e:
            print(f"DEBUG: Error in create_tenant: {e}")
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_tenants():
        # Only for admin use
        return Tenant.query.all()
