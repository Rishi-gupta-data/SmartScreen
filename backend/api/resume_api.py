import os
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from backend.services.resume_parser import ResumeParser
from backend.models.candidate import Candidate
from backend.models.db import db

resume_api = Blueprint('resume_api', __name__)
resume_parser = ResumeParser()

@resume_api.route('/resumes', methods=['POST'])
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        filename = secure_filename(file.filename)
        # Ensure the resumes directory exists
        upload_folder = current_app.config['RESUMES_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        try:
            candidate = resume_parser.process_resume(file_path)
            return jsonify({
                "message": "Resume uploaded and processed successfully",
                "candidate_id": candidate.id,
                "filename": candidate.filename
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Failed to process resume: {e}"}), 500
    return jsonify({"error": "Something went wrong"}), 500

@resume_api.route('/resumes', methods=['GET'])
def get_all_resumes():
    candidates = resume_parser.get_all_candidates()
    return jsonify([
        {"candidate_id": c.id, "filename": c.filename, "created_at": c.created_at}
        for c in candidates
    ]), 200

@resume_api.route('/resumes/<candidate_id>', methods=['GET'])
def get_resume(candidate_id):
    candidate = resume_parser.get_candidate_by_id(candidate_id)
    if candidate:
        return jsonify({
            "candidate_id": candidate.id,
            "filename": candidate.filename,
            "extracted_text": candidate.extracted_text,
            "created_at": candidate.created_at
        }), 200
    return jsonify({"error": "Candidate not found"}), 404