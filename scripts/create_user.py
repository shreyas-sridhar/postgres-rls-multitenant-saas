import os
from sqlalchemy import text, create_engine
from urllib.parse import quote_plus

# Connect as Superuser (postgres)
DB_USER = "postgres"
DB_PASS = "your_superuser_password" 
DB_HOST = "localhost"
DB_NAME = "flask_rls_saas"

APP_USER = "app_user"
APP_PASS = "app_pass_123"

def get_engine():
    uri = f"postgresql+pg8000://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}/{DB_NAME}"
    return create_engine(uri, isolation_level="AUTOCOMMIT")

def setup_app_user():
    engine = get_engine()
    print(f"Connecting as {DB_USER} to setup {APP_USER}...")
    try:
        with engine.connect() as conn:
            # Check if user exists
            result = conn.execute(text(f"SELECT 1 FROM pg_roles WHERE rolname='{APP_USER}'"))
            if not result.fetchone():
                print(f"Creating role {APP_USER}...")
                conn.execute(text(f"CREATE USER {APP_USER} WITH PASSWORD '{APP_PASS}'"))
            else:
                print(f"Role {APP_USER} already exists. Updating password...")
                conn.execute(text(f"ALTER USER {APP_USER} WITH PASSWORD '{APP_PASS}'"))

            # Grant permissions
            print("Granting permissions...")
            conn.execute(text(f"GRANT CONNECT ON DATABASE {DB_NAME} TO {APP_USER}"))
            conn.execute(text(f"GRANT USAGE ON SCHEMA public TO {APP_USER}"))
            conn.execute(text(f"GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO {APP_USER}"))
            
            # Important: Grant usage on sequences for UUID generation or others if needed (though UUID is usually random)
            # If we had serials, we would need:
            # conn.execute(text(f"GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO {APP_USER}"))

            print(f"User {APP_USER} setup complete.")

    except Exception as e:
        print(f"Error creating user: {e}")
        import sys
        sys.exit(1)
    finally:
        engine.dispose()

if __name__ == "__main__":
    setup_app_user()
