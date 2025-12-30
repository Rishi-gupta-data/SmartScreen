# backend/models/candidate.py
from .db import db
import datetime

class Candidate(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    filepath = db.Column(db.String(512), nullable=False, unique=True)
    raw_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationship to Match is implicitly created by the backref in the Match model.
    # No explicit relationship needed here if backref is used correctly in Match.
    # The backref `matches` will be available on Candidate instances.

    def __repr__(self):
        return f'<Candidate {self.filename}>'

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'filepath': self.filepath,
            'created_at': self.created_at.isoformat()
        }
