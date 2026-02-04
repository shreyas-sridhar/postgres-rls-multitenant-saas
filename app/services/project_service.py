from app.models import Project, Tenant
from app.db import db

class ProjectService:
    @staticmethod
    def create_project(tenant_id, name, description=None):
        """
        Creates a new project.
        Important: RLS policies require the transaction to have the tenant context set.
        The middleware ensures this is set before we get here.
        However, for INSERTs, RLS usually checks 'WITH CHECK'.
        Also, we must ensure we are inserting the same tenant_id as the context
        or else RLS might block it or it would be logically inconsistent.
        """
        project = Project(tenant_id=tenant_id, name=name, description=description)
        db.session.add(project)
        db.session.commit()
        return project

    @staticmethod
    def get_all_projects():
        """
        Returns all projects visible to the current tenant context.
        We do NOT need to filter by tenant_id explicitly in the query.
        Postgres RLS does it for us!
        """
        return Project.query.all()
