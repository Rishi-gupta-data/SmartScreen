import uuid
from sqlalchemy import Column, String, Integer, DateTime, func
from backend.db.connection import Base


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
