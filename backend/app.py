from flask import Flask, request, jsonify
from flask_cors import CORS
from backend import ATSBackend, BulkATSBackend
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
import os

# Load environment variables and configure logging
load_dotenv()

# Set up logging to file and console
log_file = os.path.join(os.path.dirname(__file__), 'backend.log')
file_handler = RotatingFileHandler(log_file, maxBytes=2*1024*1024, backupCount=5)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
file_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[file_handler, logging.StreamHandler()])

# Initialize Flask app with CORS
app = Flask(__name__)
CORS(app)

# Initialize backend instances
ats_backend = ATSBackend()
bulk_backend = BulkATSBackend(ats_backend)

@app.route('/', methods=['GET'])
def home():
    """Root endpoint that returns API information."""
    return jsonify({
        'status': 'online',
        'version': '1.0',
        'endpoints': {
            'analyze': '/analyze',
            'bulk_analyze': '/bulk-analyze',
            'formatting_suggestions': '/formatting-suggestions',
            'keyword_optimization': '/keyword-optimization'
        }
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_resume():
    """Endpoint for analyzing a single resume."""
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
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/bulk-analyze', methods=['POST'])
def analyze_bulk_resumes():
    """Endpoint for analyzing multiple resumes."""
    try:
        if 'resumes' not in request.files or 'job_description' not in request.form:
            return jsonify({'error': 'Missing resumes or job description'}), 400

        zip_file = request.files['resumes']
        job_description = request.form['job_description']

        bulk_backend.extract_text_from_zip(zip_file)
        results = bulk_backend.process_bulk_resumes(job_description)
        return jsonify(results)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/formatting-suggestions', methods=['POST'])
def get_formatting_suggestions():
    """Endpoint for getting resume formatting suggestions."""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'Missing resume'}), 400

        resume_file = request.files['resume']
        resume_text = ats_backend.extract_text_from_pdf(resume_file)
        suggestions = ats_backend.get_formatting_suggestions()
        return jsonify({'suggestions': suggestions})

    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/keyword-optimization', methods=['POST'])
def get_keyword_optimization():
    """Endpoint for getting keyword optimization suggestions."""
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
        logging.error(f"An unexpected error occurred: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)