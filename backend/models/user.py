import uuid
from sqlalchemy import Column, String, Integer, DateTime, func
from backend.db.connection import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    credits = Column(Integer, default=0)
    role = Column(String, default="user")  # "user" or "admin"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
