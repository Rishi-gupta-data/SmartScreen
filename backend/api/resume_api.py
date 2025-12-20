# backend/api/resume_api.py
from flask import Blueprint, request, jsonify, current_app
import logging

from backend.models.db import db
from backend.models.candidate import Candidate
from backend.utils.file_utils import save_resume_file
from backend.services.resume_parser import parse_resume_file

resume_bp = Blueprint('resume_bp', __name__)

@resume_bp.route('/', methods=['POST'])
def upload_resume():
    """
    Uploads a resume, parses it, and saves it to the database.
    Accepts multipart/form-data with a 'resume' file.
    """
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Save the physical file
        filepath, original_filename = save_resume_file(file)
        
        # Parse the text content from the saved file
        raw_text = parse_resume_file(filepath)
        
        # Check if a candidate with this exact file path already exists
        if Candidate.query.filter_by(filepath=filepath).first():
            return jsonify({'error': f'File {original_filename} has already been processed.'}), 409

        # Create a new candidate record
        new_candidate = Candidate(
            filename=original_filename,
            filepath=filepath,
            raw_text=raw_text
        )
        
        db.session.add(new_candidate)
        db.session.commit()
        
        logging.info(f"Successfully processed and saved resume: {original_filename}")
        
        return jsonify(new_candidate.to_dict()), 201

    except ValueError as e:
        logging.error(f"Validation error during resume upload: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"An unexpected error occurred during resume upload: {e}")
        # Clean up the saved file if an error occurs after saving
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': 'An internal error occurred'}), 500

@resume_bp.route('/', methods=['GET'])
def get_all_resumes():
    """
    Retrieves all candidate records from the database.
    """
    try:
        candidates = Candidate.query.all()
        return jsonify([c.to_dict() for c in candidates]), 200
    except Exception as e:
        logging.error(f"Error retrieving candidates: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500

@resume_bp.route('/<int:candidate_id>', methods=['GET'])
def get_resume(candidate_id):
    """
    Retrieves a single candidate record by its ID.
    """
    try:
        candidate = Candidate.query.get(candidate_id)
        if not candidate:
            return jsonify({'error': 'Candidate not found'}), 404
        
        candidate_data = candidate.to_dict()
        # Optionally include raw text, but be mindful of response size
        # candidate_data['raw_text'] = candidate.raw_text
        return jsonify(candidate_data), 200
    except Exception as e:
        logging.error(f"Error retrieving candidate {candidate_id}: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500
