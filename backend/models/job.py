# backend/models/job.py
from .db import db
import datetime

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Relationship to Match
    matches = db.relationship('Match', back_populates='job', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Job {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat()
        }

class Match(db.Model):
    __tablename__ = 'matches'

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Float, nullable=False)
    
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)

    # Relationships
    candidate = db.relationship('Candidate', backref=db.backref('matches', cascade='all, delete-orphan'))
    job = db.relationship('Job', back_populates='matches')

    def __repr__(self):
        return f'<Match Candidate:{self.candidate_id} Job:{self.job_id} Score:{self.score}>'

    def to_dict(self):
        return {
            'id': self.id,
            'score': self.score,
            'candidate_id': self.candidate_id,
            'job_id': self.job_id
        }
