# backend/api/match_api.py
from flask import Blueprint, request, jsonify
import logging

from backend.models.db import db
from backend.models.job import Job, Match
from backend.models.candidate import Candidate
from backend.services.matcher import matcher_service

match_bp = Blueprint('match_bp', __name__)

@match_bp.route('/job/<int:job_id>', methods=['POST'])
def run_matching_for_job(job_id):
    """
    Runs the matching process for a given job against all candidates.
    Calculates similarity scores and stores them in the database.
    """
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404

    candidates = Candidate.query.all()
    if not candidates:
        return jsonify({'error': 'No candidates found to match against'}), 404

    try:
        matches = []
        for candidate in candidates:
            # Calculate similarity
            score = matcher_service.calculate_similarity(candidate.raw_text, job.description)
            
            # Check if a match record already exists and update it, otherwise create a new one
            match_record = Match.query.filter_by(job_id=job.id, candidate_id=candidate.id).first()
            if match_record:
                match_record.score = score
            else:
                match_record = Match(
                    job_id=job.id,
                    candidate_id=candidate.id,
                    score=score
                )
                db.session.add(match_record)
            
            matches.append({
                'candidate_id': candidate.id,
                'candidate_filename': candidate.filename,
                'score': score
            })

        db.session.commit()
        
        # Sort results by score in descending order
        sorted_matches = sorted(matches, key=lambda x: x['score'], reverse=True)
        
        logging.info(f"Successfully matched {len(candidates)} candidates for job ID {job_id}.")
        
        return jsonify(sorted_matches), 200

    except Exception as e:
        logging.error(f"An unexpected error occurred during matching for job {job_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'An internal error occurred during matching'}), 500

@match_bp.route('/job/<int:job_id>', methods=['GET'])
def get_match_results(job_id):
    """
    Retrieves the stored match results for a given job, sorted by score.
    """
    job = Job.query.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
        
    try:
        # Query matches and join with candidate for more info
        results = db.session.query(Match, Candidate).join(Candidate, Match.candidate_id == Candidate.id).filter(Match.job_id == job_id).order_by(Match.score.desc()).all()

        if not results:
            return jsonify({'message': 'No match results found for this job. Run the matching process first.'}), 200

        matches_data = []
        for match, candidate in results:
            matches_data.append({
                'candidate_id': candidate.id,
                'candidate_filename': candidate.filename,
                'score': match.score
            })
        
        return jsonify(matches_data), 200

    except Exception as e:
        logging.error(f"Error retrieving match results for job {job_id}: {e}")
        return jsonify({'error': 'An internal error occurred'}), 500
