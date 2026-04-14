from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransactionOut(BaseModel):
    id: str
    type: str
    amount: int
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    transactions: list[TransactionOut]

    class Config:
        from_attributes = True
