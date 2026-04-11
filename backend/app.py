import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from flask_cors import CORS
from backend.models.db import db, init_db
from backend.api.resume_api import resume_api
from backend.api.job_api import job_api
from backend.api.match_api import match_api
from backend.api.analyze_api import analyze_api
from backend.config import config_by_name

def create_app(config_name=None):
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all origins by default

    # Use specified config or default to 'development'
    if not config_name:
        config_name = os.getenv('FLASK_ENV', 'development')

    app.config.from_object(config_by_name[config_name])
    app.config_by_name = config_by_name # Store for reference if needed

    # Initialize DB
    init_db(app)

    # Register blueprints
    app.register_blueprint(resume_api, url_prefix='/api')
    app.register_blueprint(job_api, url_prefix='/api')
    app.register_blueprint(match_api, url_prefix='/api')
    app.register_blueprint(analyze_api, url_prefix='/api')

    @app.route('/')
    def index():
        return jsonify({"message": "SmartScreen ATS Backend API"})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)