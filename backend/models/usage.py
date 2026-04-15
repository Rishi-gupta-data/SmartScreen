import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, func, JSON
from backend.db.connection import Base


class UsageLog(Base):
    """Log of API usage and credit consumption"""
    __tablename__ = "usage_logs"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)
    action = Column(String, nullable=False)  # "parse_resume", "parse_jd", "match"
    credits_used = Column(Integer, nullable=False)
    details = Column(JSON, nullable=True)  # For storing metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
