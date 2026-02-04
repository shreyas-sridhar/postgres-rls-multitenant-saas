from flask import Blueprint, request, jsonify, g
from app.services.project_service import ProjectService

project_bp = Blueprint('projects', __name__)

@project_bp.route('/', methods=['GET'])
def list_projects():
    # RLS automatically filters this
    projects = ProjectService.get_all_projects()
    return jsonify([p.to_dict() for p in projects])

@project_bp.route('/', methods=['POST'])
def create_project():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    # We rely on g.tenant_id set by middleware. 
    # If it's missing, we can't create a project linked to a tenant safely (or RLS will block).
    if not g.tenant_id:
        return jsonify({'error': 'Tenant context required'}), 400

    try:
        project = ProjectService.create_project(g.tenant_id, name, description)
        return jsonify(project.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
