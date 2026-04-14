from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class ResumeParseRequest(BaseModel):
    resume_text: str
    file_name: Optional[str] = None


class ResumeParseResponse(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    experience: List[Dict[str, str]]
    education: List[Dict[str, str]]
    raw_text: Optional[str]
    credits_deducted: int

    class Config:
        orm_mode = True


class JDParseRequest(BaseModel):
    jd_text: str
    file_name: Optional[str] = None


class JDParseResponse(BaseModel):
    title: Optional[str]
    company: Optional[str]
    required_skills: List[str]
    preferred_skills: List[str]
    experience_required: Optional[str]
    salary_range: Optional[str]
    qualifications: List[str]
    responsibilities: List[str]
    raw_text: Optional[str]
    credits_deducted: int

    class Config:
        orm_mode = True


class MatchRequest(BaseModel):
    resume_data: Dict[str, Any]
    jd_data: Dict[str, Any]


class MatchResponse(BaseModel):
    match_score: float
    skill_match: Dict[str, Any]
    experience_match: str
    education_match: str
    overall_recommendation: str
    missing_skills: List[str]
    bonus_skills: List[str]
    credits_deducted: int

    class Config:
        orm_mode = True
