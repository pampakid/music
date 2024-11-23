from flask import Flask
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
    from .routes import video
    app.register_blueprint(video.video_bp, url_prefix='/api/v1/video')
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200
    
    return app