from pydantic import BaseModel
from typing import Optional


class ResumeParseRequest(BaseModel):
    resume_text: str
    filename: Optional[str] = None


class JDParseRequest(BaseModel):
    jd_text: str
    filename: Optional[str] = None


class MatchRequest(BaseModel):
    resume_text: str
    jd_text: str


class BuyCreditRequest(BaseModel):
    amount: int  # Number of credits to buy


class TransactionResponse(BaseModel):
    id: str
    user_id: str
    type: str  # "add", "deduct", etc.
    amount: int
    description: Optional[str]
    created_at: str


class CreditsResponse(BaseModel):
    user_id: str
    current_balance: int
    total_used: int
    total_purchased: int


class ResumeParseResponse(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: list
    experience: list
    education: list
    credits_used: int
    remaining_credits: int


class JDParseResponse(BaseModel):
    title: Optional[str]
    company: Optional[str]
    required_skills: list
    preferred_skills: list
    experience_required: Optional[str]
    salary_range: Optional[str]
    qualifications: list
    responsibilities: list
    credits_used: int
    remaining_credits: int


class MatchResponse(BaseModel):
    match_score: float
    skill_match: dict
    experience_match: str
    education_match: str
    overall_recommendation: str
    missing_skills: list
    bonus_skills: list
    credits_used: int
    remaining_credits: int
