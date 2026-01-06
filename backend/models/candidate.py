import uuid
from datetime import datetime
from backend.models.db import db

class Candidate(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)
    embedding = db.Column(db.PickleType, nullable=True) # To store spaCy vector
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Candidate {self.filename}>"