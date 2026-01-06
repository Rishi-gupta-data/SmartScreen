from flask import Blueprint, request, jsonify
from backend.services.matcher import Matcher
from backend.services.job_parser import JobParser
from backend.services.resume_parser import ResumeParser
from backend.models.db import db

match_api = Blueprint('match_api', __name__)
matcher = Matcher()
job_parser = JobParser()
resume_parser = ResumeParser()

@match_api.route('/match/<job_id>', methods=['GET'])
def get_matches_for_job(job_id):
    job = job_parser.get_job_by_id(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    candidates = resume_parser.get_all_candidates()
    
    if not candidates:
        return jsonify({"message": "No candidates available to match"}), 200

    ranked_matches = matcher.match_candidates_to_job(job, candidates)
    
    return jsonify({
        "job_id": job_id,
        "job_title": job.title,
        "matches": ranked_matches
    }), 200