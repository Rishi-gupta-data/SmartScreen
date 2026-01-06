import spacy
from backend.models.db import db
from backend.models.job import Job

class JobParser:
    def __init__(self):
        # Load the spaCy model
        try:
            self.nlp = spacy.load("en_core_web_md")
        except OSError:
            print("Downloading spaCy model 'en_core_web_md'...")
            spacy.cli.download("en_core_web_md")
            self.nlp = spacy.load("en_core_web_md")

    def process_job_description(self, title: str, description: str) -> Job:
        """
        Saves a job description and generates its embedding.
        """
        if not description:
            raise ValueError("Job description cannot be empty.")

        # Generate embedding
        doc = self.nlp(description)
        embedding = doc.vector.tobytes() # Store as bytes for PickleType

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
