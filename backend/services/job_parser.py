import os
from sentence_transformers import SentenceTransformer
from backend.models.db import db
from backend.models.job import Job

class JobParser:
    def __init__(self):
        # Load the sentence-transformer model
        model_name = os.getenv("HF_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)

    def process_job_description(self, title: str, description: str) -> Job:
        """
        Saves a job description and generates its embedding.
        """
        if not description:
            raise ValueError("Job description cannot be empty.")

        # Generate embedding using SentenceTransformer
        embedding_vec = self.model.encode(description)
        embedding = embedding_vec.tobytes() # Store as bytes for PickleType

        job = Job(
            title=title,
            description=description,
            embedding=embedding
        )
        db.session.add(job)
        db.session.commit()
        return job

    def get_job_by_id(self, job_id: str) -> Job:
        return Job.query.get(job_id)

    def get_all_jobs(self):
        return Job.query.all()
