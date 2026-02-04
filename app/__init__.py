from flask import Flask, jsonify
from app.config import Config
from app.db import db
from app.routes import project_bp, tenant_bp
from app.middleware import register_middleware

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register Middleware
    register_middleware(app)

    # Register Blueprints
    app.register_blueprint(project_bp, url_prefix='/api/projects')
    app.register_blueprint(tenant_bp, url_prefix='/api/tenants')

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'}), 200

    return app
