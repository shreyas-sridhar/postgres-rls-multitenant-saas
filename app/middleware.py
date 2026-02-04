from flask import request, g, current_app, jsonify
from app.db import set_tenant_context

def register_middleware(app):
    @app.before_request
    def tenant_context_middleware():
        # Skip for static files or health checks if any (optional)
        if request.endpoint and 'static' in request.endpoint:
            return

        # Extract tenant_id from header
        tenant_id = request.headers.get(app.config['TENANT_HEADER'])

        if tenant_id:
            # Validate UUID format loosely or strict?
            # For now, we trust it's a UUID string. 
            # If invalid UUID is passed, Postgres might throw an error when we try to cast in policy,
            # or we catch it here.
            try:
                set_tenant_context(tenant_id)
                g.tenant_id = tenant_id # Store in g for application usage if needed (e.g. logging)
            except Exception as e:
                import traceback
                traceback.print_exc()
                current_app.logger.error(f"Middleware Error setting tenant {tenant_id}: {e}")
                return jsonify({"error": f"Invalid Tenant ID or Database Error: {e}"}), 500
        else:
            # Depending on reqs, we might block access or allow "public" access.
            # RLS policies usually default to "deny all" or "empty" if the variable is not set
            # unless we have a policy for NULL.
            # Our policy: using (tenant_id = current_setting(...))
            # If current_setting is missing/null, it might fail or return nothing.
            # In 'init_db.sql' creating the policy with 'current_setting(..., true)' returns NULL if missing.
            # tenant_id=NULL rows? (We don't have them based on schema).
            # So effectively, no tenant_id means NO access to rows.
            g.tenant_id = None
            current_app.logger.warning("No X-Tenant-ID header found. RLS context empty.")
