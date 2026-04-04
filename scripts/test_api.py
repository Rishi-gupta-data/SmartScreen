import requests
import json
import time
import os

BASE_URL = "http://127.0.0.1:5000/api"

def test_api():
    print("--- Starting API Tests ---")
    
    # 1. Check root
    try:
        response = requests.get("http://127.0.0.1:5000/")
        print(f"Root endpoint: {response.status_code}, {response.json()}")
    except Exception as e:
        print(f"Failed to connect to backend: {e}")
        return

    # 2. Create a Job
    job_data = {
        "title": "Senior Python Developer",
        "description": "Looking for a Senior Python Developer with experience in Flask, SQLAlchemy, and NLP. Should know Sentence Transformers and vector embeddings."
    }
    response = requests.post(f"{BASE_URL}/jobs", json=job_data)
    print(f"Create Job: {response.status_code}")
    job_id = response.json().get('job_id')
    print(f"Job ID: {job_id}")

    # 3. Upload a Resume (Mocked as a text file for simplicity)
    # Since the system handles PDF/DOCX, I'll use a small PDF from the data folder if available
    resume_path = "data/resumes/1f686cab-34b5-4210-a43b-7409ac7c3326.pdf"
    if os.path.exists(resume_path):
        with open(resume_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"{BASE_URL}/resumes", files=files)
            print(f"Upload Resume: {response.status_code}")
            if response.status_code == 201:
                candidate_id = response.json().get('candidate_id')
                print(f"Candidate ID: {candidate_id}")
            else:
                print(f"Error: {response.json()}")
    else:
        print(f"Resume file not found at {resume_path}")

    # 4. Get Matches
    if job_id:
        response = requests.get(f"{BASE_URL}/match/{job_id}")
        print(f"Get Matches: {response.status_code}")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.json()}")

if __name__ == "__main__":
    test_api()
