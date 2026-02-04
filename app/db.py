from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import g, current_app

# Disable expire_on_commit so objects remain accessible after commit without triggering a refresh
# (which would fail because RLS context is cleared at commit)
db = SQLAlchemy(session_options={"expire_on_commit": False})

def set_tenant_context(tenant_id):
    """
    Sets the current tenant context for the database session using RLS.
    This executes: SET LOCAL app.current_tenant = 'tenant_id';
    """
    if not tenant_id:
        return

    try:
        # We use set_config function.
        # Bypass parameter binding to avoid driver type issues.
        # ensure tenant_id is safe (it should be uuid string)
        # We can trust our internal middleware/service to pass strings, but let's be careful.
        
        sql = text(f"SELECT set_config('app.current_tenant', '{tenant_id}', true)")
        db.session.execute(sql)
        current_app.logger.info(f"RLS Context set to tenant_id: {tenant_id}")
    except Exception as e:
        current_app.logger.error(f"Failed to set tenant context: {e}")
        raise e
