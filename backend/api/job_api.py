# backend/api/job_api.py
from flask import Blueprint, request, jsonify
import logging

from backend.models.db import db
from backend.models.job import Job

job_bp = Blueprint('job_bp', __name__)

@job_bp.route('/', methods=['POST'])
def create_job():
    """
    Creates a new job description record.
    Accepts a JSON payload with 'title' and 'description'.
    """
    data = request.get_json()
    if not data or not data.get('title') or not data.get('description'):
        return jsonify({'error': 'Missing title or description in request body'}), 400

    try:
        new_job = Job(
            title=data['title'],
            description=data['description']
        )
        
        db.session.add(new_job)
        db.session.commit()
        
        logging.info(f"Successfully created job: {new_job.title}")
        
        return jsonify(new_job.to_dict()), 201

    except Exception as e:
        logging.error(f"An unexpected error occurred during job creation: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500

@job_bp.route('/', methods=['GET'])
def get_all_jobs():
    """
    Retrieves all job records from the database.
    """
    try:
        jobs = Job.query.all()
        return jsonify([j.to_dict() for j in jobs]), 200
    except Exception as e:
        logging.error(f"Error retrieving jobs: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500

@job_bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """
    Retrieves a single job record by its ID.
    """
    try:
        job = Job.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify(job.to_dict()), 200
    except Exception as e:
        logging.error(f"Error retrieving job {job_id}: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500
