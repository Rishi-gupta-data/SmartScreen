import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from flask_cors import CORS
from backend.models.db import db, init_db
from backend.api.resume_api import resume_api
from backend.api.job_api import job_api
from backend.api.match_api import match_api
from backend.api.llm_api import llm_api

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all origins by default

    # Configuration
    database_path = os.path.join(app.root_path, '..', 'data', 'ats.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.abspath(database_path)}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, '../data/resumes')
    app.config['JOB_DESCRIPTION_FOLDER'] = os.path.join(app.root_path, '../data/jobs')

    # Initialize DB
    init_db(app)

    # Register blueprints
    app.register_blueprint(resume_api, url_prefix='/api')
    app.register_blueprint(job_api, url_prefix='/api')
    app.register_blueprint(match_api, url_prefix='/api')
    app.register_blueprint(llm_api, url_prefix='/api')

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
    app.run(debug=True)