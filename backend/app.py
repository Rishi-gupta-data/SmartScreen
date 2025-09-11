import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import ATSBackend, BulkATSBackend

load_dotenv()

log_file = os.path.join(os.path.dirname(__file__), 'backend.log')
file_handler = RotatingFileHandler(log_file, maxBytes=2 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
file_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, logging.StreamHandler()]
)

app = Flask(__name__)
CORS(app)

ats_backend = ATSBackend()
bulk_backend = BulkATSBackend(ats_backend)

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    try:
        if 'resume' not in request.files or 'job_description' not in request.form:
            return jsonify({'error': 'Missing resume or job description'}), 400

        resume_file = request.files['resume']
        job_description = request.form['job_description']

        resume_text = ats_backend.extract_text_from_pdf(resume_file)
        ats_backend.set_job_description(job_description)
        analysis = ats_backend.analyze_resume(resume_text, job_description)

        return jsonify(analysis)

    except Exception as e:
        logging.error(f"An unexpected error occurred in /api/analyze: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500


@app.route('/api/bulk-analyze', methods=['POST'])
def analyze_bulk_resumes():
    try:
        if 'resumes' not in request.files or 'job_description' not in request.form:
            return jsonify({'error': 'Missing resumes ZIP file or job description'}), 400

        zip_file = request.files['resumes']
        job_description = request.form['job_description']

        bulk_backend.extract_text_from_zip(zip_file)
        results = bulk_backend.process_bulk_resumes(job_description)

        return jsonify(results)

    except Exception as e:
        logging.error(f"An unexpected error occurred in /api/bulk-analyze: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500


@app.route('/api/formatting-suggestions', methods=['POST'])
def get_formatting_suggestions():
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'Missing resume file'}), 400

        resume_file = request.files['resume']
        resume_text = ats_backend.extract_text_from_pdf(resume_file)
        suggestions = ats_backend.get_formatting_suggestions()

        return jsonify({'suggestions': suggestions})

    except Exception as e:
        logging.error(f"An unexpected error occurred in /api/formatting-suggestions: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500


@app.route('/api/keyword-optimization', methods=['POST'])
def get_keyword_optimization():
    try:
        if 'resume' not in request.files or 'job_description' not in request.form:
            return jsonify({'error': 'Missing resume or job description'}), 400

        resume_file = request.files['resume']
        job_description = request.form['job_description']

        resume_text = ats_backend.extract_text_from_pdf(resume_file)
        ats_backend.set_job_description(job_description)
        optimization = ats_backend.get_keyword_optimization()

        return jsonify({'optimization': optimization})

    except Exception as e:
        logging.error(f"An unexpected error occurred in /api/keyword-optimization: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)