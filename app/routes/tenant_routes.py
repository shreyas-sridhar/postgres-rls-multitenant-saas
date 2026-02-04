from flask import Blueprint, request, jsonify
from app.services.tenant_service import TenantService

tenant_bp = Blueprint('tenants', __name__)

@tenant_bp.route('/', methods=['POST'])
def create_tenant():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400
        
    try:
        tenant = TenantService.create_tenant(name)
        return jsonify(tenant.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tenant_bp.route('/', methods=['GET'])
def list_tenants():
    # Helper to see tenants (should ideally be admin only)
    tenants = TenantService.get_all_tenants()
    return jsonify([t.to_dict() for t in tenants])
