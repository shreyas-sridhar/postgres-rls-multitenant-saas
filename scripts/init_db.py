import os
import sqlalchemy
from sqlalchemy import text, create_engine
from urllib.parse import quote_plus

# Database Config
DB_USER = "postgres"
DB_PASS = "your_password"  # Start with generic, let user set it via env or edit
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "flask_rls_saas"

# Reading SQL init script
INIT_SQL_PATH = os.path.join(os.path.dirname(__file__), 'init_db.sql')

def get_engine(dbname="postgres"):
    uri = f"postgresql+pg8000://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{dbname}"
    return create_engine(uri, isolation_level="AUTOCOMMIT")

def create_database():
    print(f"Connecting to 'postgres' database to check/create '{DB_NAME}'...")
    engine = get_engine("postgres")
    try:
        with engine.connect() as conn:
            # Check if DB exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'"))
            if result.fetchone():
                print(f"Database '{DB_NAME}' already exists.")
            else:
                print(f"Creating database '{DB_NAME}'...")
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                print("Database created successfully.")
    except Exception as e:
        print(f"Error checking/creating database: {e}")
        import sys
        sys.exit(1)
    finally:
        engine.dispose()

def run_init_sql():
    print(f"Applying schema from {INIT_SQL_PATH} to '{DB_NAME}'...")
    if not os.path.exists(INIT_SQL_PATH):
        print(f"Error: SQL file not found at {INIT_SQL_PATH}")
        return

    with open(INIT_SQL_PATH, 'r') as f:
        sql_content = f.read()

    engine = get_engine(DB_NAME)
    try:
        with engine.connect() as conn:
            # sqlalchemy might fail with multiple statements in one execute call depending on driver
            # pg8000 usually handles it, or we split.
            # Let's try executing the whole block.
            # If it fails, we might need to split by ';'
            conn.execute(text(sql_content))
            print("Schema applied successfully (Tables created, RLS enabled).")
    except Exception as e:
        print(f"Error applying SQL: {e}")
    finally:
        engine.dispose()

if __name__ == "__main__":
    create_database()
    run_init_sql()
