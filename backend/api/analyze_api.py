import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from backend.services.resume_parser import ResumeParser
from backend.services.job_parser import JobParser
from backend.services.matcher import Matcher
from backend.models.candidate import Candidate
from backend.models.job import Job
from backend.models.db import db
from backend.utils.file_utils import extract_text_from_file
from sentence_transformers import SentenceTransformer
import numpy as np

analyze_api = Blueprint('analyze_api', __name__)
resume_parser = ResumeParser()
job_parser = JobParser()
matcher = Matcher()

# Keywords database for skill extraction
SKILL_KEYWORDS = {
    'Python': ['python', 'django', 'flask', 'fastapi'],
    'JavaScript': ['javascript', 'js', 'nodejs', 'node.js', 'react', 'angular', 'vue'],
    'Java': ['java', 'spring', 'j2ee'],
    'SQL': ['sql', 'postgresql', 'mysql', 'mongodb', 'database'],
    'AWS': ['aws', 'amazon web services', 'ec2', 's3', 'lambda'],
    'Docker': ['docker', 'kubernetes', 'k8s', 'containers'],
    'Machine Learning': ['machine learning', 'ml', 'tensorflow', 'pytorch', 'sklearn', 'scikit-learn'],
    'NLP': ['nlp', 'natural language processing', ' nltk', 'spacy', 'transformers'],
    'Git': ['git', 'github', 'gitlab', 'version control'],
    'CI/CD': ['ci/cd', 'jenkins', 'github actions', 'gitlab ci'],
    'Agile': ['agile', 'scrum', 'kanban', 'sprint'],
    'Communication': ['communication', 'presentation', 'teamwork', 'collaboration'],
    'Leadership': ['leadership', 'management', 'team lead', 'mentor'],
    'Problem Solving': ['problem solving', 'analytical', 'critical thinking'],
}

def extract_skills(text):
    """Extract skills from text based on keyword matching."""
    text_lower = text.lower()
    found_skills = []
    missing_skills = []
    
    for skill, keywords in SKILL_KEYWORDS.items():
        if any(keyword.lower() in text_lower for keyword in keywords):
            found_skills.append(skill)
        else:
            missing_skills.append(skill)
    
    return found_skills, missing_skills

def calculate_match_percentage(job_text, resume_text):
    """Calculate match percentage based on semantic similarity and keyword matching."""
    # Get semantic similarity
    model = SentenceTransformer(os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))
    job_embedding = model.encode(job_text)
    resume_embedding = model.encode(resume_text)
    
    # Calculate cosine similarity
    similarity = np.dot(job_embedding, resume_embedding) / (np.linalg.norm(job_embedding) * np.linalg.norm(resume_embedding))
    
    # Get keyword match
    found_skills, missing_skills = extract_skills(resume_text)
    job_found, job_missing = extract_skills(job_text)
    
    # If job mentions specific skills, calculate keyword match ratio
    if job_found:
        keyword_match = len([s for s in job_found if s in found_skills]) / len(job_found)
    else:
        keyword_match = similarity  # Fall back to semantic similarity
    
    # Combined score: 60% semantic + 40% keyword
    combined_score = 0.6 * similarity + 0.4 * keyword_match
    
    return round(combined_score * 100, 1)

def generate_suggestions(found_skills, missing_skills, resume_text):
    """Generate improvement suggestions based on analysis."""
    suggestions = []
    
    if missing_skills:
        suggestions.append(f"Consider adding experience or skills in: {', '.join(missing_skills[:5])}")
    
    if len(resume_text.split()) < 500:
        suggestions.append("Your resume might be too short. Consider adding more details about your projects and achievements.")
    
    if not any(word in resume_text.lower() for word in ['project', 'achievement', 'accomplishment']):
        suggestions.append("Add specific projects and achievements with measurable outcomes.")
    
    if not any(word in resume_text.lower() for word in ['percent', '%', 'increased', 'improved', 'reduced']):
        suggestions.append("Include quantifiable metrics and results (e.g., 'improved performance by 30%').")
    
    return suggestions

@analyze_api.route('/analyze', methods=['POST'])
def analyze_resume():
    """Analyze a single resume against a job description."""
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    
    if 'job_description' not in request.form:
        return jsonify({"error": "No job description provided"}), 400
    
    resume_file = request.files['resume']
    job_description = request.form.get('job_description', '')
    
    if resume_file.filename == '':
        return jsonify({"error": "No resume file selected"}), 400
    
    try:
        # Save and process resume
        filename = secure_filename(resume_file.filename)
        upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'resumes')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        resume_file.save(file_path)
        
        # Extract text from resume
        resume_text = extract_text_from_file(file_path)
        if not resume_text:
            return jsonify({"error": "Could not extract text from resume"}), 400
        
        # Generate embedding for resume
        model = SentenceTransformer(os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))
        resume_embedding = model.encode(resume_text).tobytes()
        
        # Generate embedding for job description
        job_embedding = model.encode(job_description).tobytes()
        
        # Calculate similarity
        similarity = matcher.calculate_similarity(job_embedding, resume_embedding)
        match_percentage = round(similarity * 100, 1)
        
        # Extract skills
        found_skills, missing_skills = extract_skills(resume_text)
        job_found_skills, _ = extract_skills(job_description)
        
        # Filter found skills to only those mentioned in job
        matched_keywords = [s for s in found_skills if s in job_found_skills or s in found_skills]
        
        # Generate suggestions
        suggestions = generate_suggestions(found_skills, missing_skills, resume_text)
        
        # Determine suitability
        suitability = "Suitable" if match_percentage >= 70 else "Not Suitable"
        
        result = {
            "score": match_percentage,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_skills[:10],
            "suggestions": suggestions,
            "suitability": suitability,
            "key_strengths": found_skills[:5],
            "areas_for_improvement": missing_skills[:5],
            "formatting_tips": [
                "Use a clean, professional font like Arial or Calibri",
                "Keep consistent formatting throughout",
                "Use bullet points for better readability",
                "Include action verbs at the start of each bullet point"
            ]
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to analyze resume: {str(e)}"}), 500


@analyze_api.route('/bulk-analyze', methods=['POST'])
def bulk_analyze():
    """Analyze multiple resumes (ZIP file) against a job description."""
    if 'resumes' not in request.files:
        return jsonify({"error": "No resumes file provided"}), 400
    
    if 'job_description' not in request.form:
        return jsonify({"error": "No job description provided"}), 400
    
    resumes_file = request.files['resumes']
    job_description = request.form.get('job_description', '')
    
    if resumes_file.filename == '':
        return jsonify({"error": "No resumes file selected"}), 400
    
    try:
        import zipfile
        import tempfile
        import io
        
        # Read ZIP file
        zip_data = io.BytesIO(resumes_file.read())
        
        results = []
        model = SentenceTransformer(os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2"))
        job_embedding = model.encode(job_description).tobytes()
        
        with zipfile.ZipFile(zip_data, 'r') as zip_ref:
            for file_info in zip_ref.namelist():
                if file_info.lower().endswith(('.pdf', '.docx')):
                    try:
                        # Extract file to temp location
                        with zip_ref.open(file_info) as pdf_file:
                            # Read content
                            temp_path = os.path.join(tempfile.gettempdir(), os.path.basename(file_info))
                            with open(temp_path, 'wb') as f:
                                f.write(pdf_file.read())
                        
                        # Extract text
                        resume_text = extract_text_from_file(temp_path)
                        if not resume_text:
                            continue
                        
                        # Generate embedding
                        resume_embedding = model.encode(resume_text).tobytes()
                        
                        # Calculate similarity
                        similarity = matcher.calculate_similarity(job_embedding, resume_embedding)
                        match_percentage = round(similarity * 100, 1)
                        
                        # Extract skills
                        found_skills, missing_skills = extract_skills(resume_text)
                        job_found_skills, _ = extract_skills(job_description)
                        
                        # Determine suitability
                        suitability = "Suitable" if match_percentage >= 70 else "Not Suitable"
                        
                        results.append({
                            "name": os.path.basename(file_info),
                            "Match Percentage": match_percentage,
                            "Suitability": suitability,
                            "Found Keywords": found_skills[:10],
                            "Missing Keywords": missing_skills[:10],
                            "Key Strengths": found_skills[:5],
                            "Areas for Improvement": missing_skills[:5],
                            "Resume Formatting & Optimization Tips": [
                                "Use consistent formatting",
                                "Add quantifiable achievements",
                                "Include relevant keywords"
                            ]
                        })
                        
                        # Clean up temp file
                        os.remove(temp_path)
                        
                    except Exception as e:
                        print(f"Error processing {file_info}: {e}")
                        continue
        
        # Sort by match percentage (highest first)
        results.sort(key=lambda x: x["Match Percentage"], reverse=True)
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to analyze resumes: {str(e)}"}), 500