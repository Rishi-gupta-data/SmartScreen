from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer
from typing import Optional
from datetime import datetime


class AdminCreate(BaseModel):
    """Schema for creating a new admin"""
    email: EmailStr
    password: str


class AdminUpdate(BaseModel):
    """Schema for updating admin details"""
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class AdminResponse(BaseModel):
    """Schema for admin response"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    email: str
    created_at: Optional[datetime] = None
    
    @field_serializer('created_at')
    def serialize_created_at(self, value: Optional[datetime], _info):
        """Serialize datetime to ISO format string"""
        return value.isoformat() if value else None


class AdminListResponse(BaseModel):
    """Schema for listing admins"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    email: str
    created_at: Optional[datetime] = None
    
    @field_serializer('created_at')
    def serialize_created_at(self, value: Optional[datetime], _info):
        """Serialize datetime to ISO format string"""
        return value.isoformat() if value else None


class AdminStats(BaseModel):
    """Schema for admin dashboard stats"""
    total_users: int
    total_admins: int
    total_credits_sold: int
    total_transactions: int
    recent_signups: int
