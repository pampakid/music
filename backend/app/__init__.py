# app/__init__.py
from flask import Flask, jsonify, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Register blueprints
    from .routes.video import video_bp
    app.register_blueprint(video_bp, url_prefix='/api/v1/video')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
        
    @app.route('/debug/routes')
    def list_routes():
        routes = []
        for rule in app.url_map.iter_rules():
            try:
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'path': str(rule)
                })
            except Exception as e:
                continue
        return jsonify(routes)
    
    return app