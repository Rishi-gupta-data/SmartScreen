from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


# ── Resume ────────────────────────────────────────────────────────────────

class ResumeParseRequest(BaseModel):
    resume_text: str
    file_name: Optional[str] = Field(default=None, alias="filename")
    
    class Config:
        populate_by_name = True  # Accept both file_name and filename


class ExperienceEntry(BaseModel):
    company: str
    role: str
    duration: str


class EducationEntry(BaseModel):
    degree: str
    institution: str
    field: str
    year: str

class FitmentCategory(BaseModel):
    emoji: Optional[str] = None
    label: Optional[str] = None


class ResumeParseResponse(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    skills: List[str] = []
    experience: List[ExperienceEntry] = []
    total_experience_years: Optional[float] = None   # ✅ was required
    experience_level: Optional[str] = None           # ✅ was required
    education: List[EducationEntry] = []
    raw_text: Optional[str] = None
    credits_deducted: int

    class Config:
        from_attributes = True


# ── Job Description ───────────────────────────────────────────────────────

class JDParseRequest(BaseModel):
    jd_text: str
    file_name: Optional[str] = Field(default=None, alias="filename")
    
    class Config:
        populate_by_name = True  # Accept both file_name and filename


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
        from_attributes = True


# ── Match ─────────────────────────────────────────────────────────────────

class MatchRequest(BaseModel):
    resume_data: Dict[str, Any]
    jd_data: Dict[str, Any]


class SkillMatchDetail(BaseModel):
    required_matched: List[str]
    required_missing: List[str]
    preferred_matched: List[str]
    preferred_missing: List[str]
    extra_skills: List[str]
    match_percentage: float


class ScoreBreakdown(BaseModel):
    skill_score: float
    experience_score: float
    education_score: float
    weights: Dict[str, str]


class MatchResponse(BaseModel):
    match_score: float
    breakdown: ScoreBreakdown
    skill_match: SkillMatchDetail
    experience_match: str
    education_match: str
    overall_recommendation: str
    recommendation_detail: str
    improvement_tips: List[str]
    credits_deducted: int
    fitment_category: Optional[FitmentCategory] = None

    class Config:
        from_attributes = True