import os

class Config:
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Using a default local postgres connection string, but can be overridden by env var
    # Ensure this database exists!
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+pg8000://app_user:app_pass_123@localhost/flask_rls_saas')
    
    # RLS specific config
    TENANT_HEADER = 'X-Tenant-ID'
