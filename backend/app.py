# backend/app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from backend.config import config_by_name
from backend.models.db import db  # Import the db instance

def create_app(config_name='default'):
    """
    Application factory function.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Initialize extensions
    CORS(app)
    db.init_app(app)
    
    # Initialize config static method if any
    config_by_name[config_name].init_app(app)

    # Register blueprints
    from .api.resume_api import resume_bp
    from .api.job_api import job_bp
    from .api.match_api import match_bp
    
    app.register_blueprint(resume_bp, url_prefix='/api/resumes')
    app.register_blueprint(job_bp, url_prefix='/api/jobs')
    app.register_blueprint(match_bp, url_prefix='/api/match')

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

    @app.route('/health')
    def health_check():
        return "OK", 200

    return app
