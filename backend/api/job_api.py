import os
from flask import Blueprint, request, jsonify
from backend.services.job_parser import JobParser
from backend.models.job import Job

job_api = Blueprint('job_api', __name__)
job_parser = JobParser()

@job_api.route('/jobs', methods=['POST'])
def create_job():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    try:
        job = job_parser.process_job_description(title, description)
        return jsonify({
            "message": "Job description processed successfully",
            "job_id": job.id,
            "title": job.title
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to process job description: {e}"}), 500

@job_api.route('/jobs', methods=['GET'])
def get_all_jobs():
    jobs = job_parser.get_all_jobs()
    return jsonify([
        {"job_id": j.id, "title": j.title, "created_at": j.created_at}
        for j in jobs
    ]), 200

@job_api.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    job = job_parser.get_job_by_id(job_id)
    if job:
        return jsonify({
            "job_id": job.id,
            "title": job.title,
            "description": job.description,
            "created_at": job.created_at
        }), 200
    return jsonify({"error": "Job not found"}), 404