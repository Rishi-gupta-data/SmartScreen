import re
from typing import List, Dict, Any, Optional


def parse_resume(resume_text: str) -> Dict[str, Any]:
    """
    Placeholder resume parser that extracts basic info using regex patterns.
    TODO: Replace with HuggingFace model for production use.
    """
    parsed = {
        "name": extract_name(resume_text),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "skills": extract_skills(resume_text),
        "experience": extract_experience(resume_text),
        "education": extract_education(resume_text),
        "raw_text": resume_text[:500],  # Store first 500 chars
    }
    return parsed


def parse_jd(jd_text: str) -> Dict[str, Any]:
    """
    Placeholder JD parser that extracts basic info using regex patterns.
    TODO: Replace with HuggingFace model for production use.
    """
    parsed = {
        "title": extract_job_title(jd_text),
        "company": extract_company(jd_text),
        "required_skills": extract_required_skills(jd_text),
        "preferred_skills": extract_preferred_skills(jd_text),
        "experience_required": extract_experience_requirement(jd_text),
        "salary_range": extract_salary(jd_text),
        "qualifications": extract_qualifications(jd_text),
        "responsibilities": extract_responsibilities(jd_text),
        "raw_text": jd_text[:500],  # Store first 500 chars
    }
    return parsed


def match_resume_to_jd(resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate match score and generate recommendations.
    TODO: Use advanced ML models for better matching.
    """
    resume_skills = set(s.lower() for s in resume_data.get("skills", []))
    required_skills = set(s.lower() for s in jd_data.get("required_skills", []))
    preferred_skills = set(s.lower() for s in jd_data.get("preferred_skills", []))
    
    # Calculate skill match
    required_match = resume_skills & required_skills
    preferred_match = resume_skills & preferred_skills
    
    # Calculate match score (0-100)
    if not required_skills:
        skill_score = 100
    else:
        skill_score = (len(required_match) / len(required_skills)) * 100
    
    # Bonus points for preferred skills (max +20)
    bonus_score = min((len(preferred_match) / max(len(preferred_skills), 1)) * 20, 20)
    
    match_score = min(skill_score + bonus_score, 100)
    
    # Generate recommendation
    if match_score >= 80:
        recommendation = "Excellent Match - Highly Recommended"
    elif match_score >= 60:
        recommendation = "Good Match - Recommended"
    elif match_score >= 40:
        recommendation = "Moderate Match - Consider"
    else:
        recommendation = "Poor Match - Not Recommended"
    
    return {
        "match_score": round(match_score, 2),
        "skill_match": {
            "required_matched": list(required_match),
            "preferred_matched": list(preferred_match),
            "match_percentage": round(skill_score, 2),
        },
        "experience_match": "Not analyzed (placeholder)",
        "education_match": "Not analyzed (placeholder)",
        "overall_recommendation": recommendation,
        "missing_skills": list(required_skills - resume_skills),
        "bonus_skills": list(preferred_match),
    }


def extract_name(text: str) -> Optional[str]:
    """Extract name from resume text"""
    # Look for name patterns (simple heuristic)
    lines = text.split("\n")
    if lines:
        first_line = lines[0].strip()
        if len(first_line) < 100 and first_line.isupper():
            return first_line
    return None


def extract_email(text: str) -> Optional[str]:
    """Extract email from text"""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text"""
    match = re.search(r"\+?[1-9]\d{1,14}", text)
    return match.group(0) if match else None


def extract_skills(text: str) -> List[str]:
    """Extract skills from resume using keyword matching"""
    skills_keywords = [
        "python", "java", "c++", "javascript", "typescript", "react", "angular",
        "vue", "nodejs", "django", "flask", "fastapi", "spring", "sql", "nosql",
        "mongodb", "postgresql", "aws", "gcp", "azure", "docker", "kubernetes",
        "git", "github", "gitlab", "devops", "ci/cd", "jenkins", "linux", "windows",
        "machine learning", "deep learning", "tensorflow", "keras", "nlp", "cv",
        "pandas", "numpy", "scikit-learn", "rest", "api", "graphql", "soap",
        "agile", "scrum", "jira", "confluence", "html", "css", "sass", "bootstrap",
    ]
    text_lower = text.lower()
    found_skills = []
    for skill in skills_keywords:
        if skill in text_lower:
            found_skills.append(skill)
    return list(set(found_skills))


def extract_experience(text: str) -> List[Dict[str, str]]:
    """Extract work experience from resume"""
    # Placeholder: returns empty list or simulated data
    # In production, use NER models for better extraction
    experience = []
    if "experience" in text.lower() or "worked" in text.lower():
        experience = [
            {"company": "Unknown", "role": "Unknown", "duration": "Unknown"}
        ]
    return experience


def extract_education(text: str) -> List[Dict[str, str]]:
    """Extract education from resume"""
    # Placeholder: returns empty list or simulated data
    education = []
    if "degree" in text.lower() or "university" in text.lower() or "b.tech" in text.lower():
        education = [{"institution": "Unknown", "degree": "Unknown", "field": "Unknown"}]
    return education


def extract_job_title(text: str) -> Optional[str]:
    """Extract job title from JD"""
    lines = text.split("\n")
    for line in lines[:5]:  # Check first 5 lines
        line = line.strip()
        if len(line) < 100 and ("position" not in line.lower() or any(
            keyword in line.lower() for keyword in
            ["engineer", "developer", "analyst", "manager", "lead", "architect"]
        )):
            return line
    return None


def extract_company(text: str) -> Optional[str]:
    """Extract company name from JD"""
    # Simple heuristic
    if "company" in text.lower():
        match = re.search(r"Company:\s*([^\n]+)", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_required_skills(text: str) -> List[str]:
    """Extract required skills from JD"""
    return extract_skills(text)


def extract_preferred_skills(text: str) -> List[str]:
    """Extract preferred skills from JD"""
    # Look for "preferred" or "nice to have" sections
    preferred = []
    if "preferred" in text.lower() or "nice to have" in text.lower():
        # In production, use better NLP
        preferred = extract_skills(text)[: len(extract_skills(text)) // 2]
    return preferred


def extract_experience_requirement(text: str) -> Optional[str]:
    """Extract experience requirement from JD"""
    match = re.search(r"(\d+)\s*(?:\+)?\s*(?:years?|yrs?)", text, re.IGNORECASE)
    if match:
        return f"{match.group(1)}+ years"
    return None


def extract_salary(text: str) -> Optional[str]:
    """Extract salary range from JD"""
    match = re.search(r"(\$|₹|€)[0-9,]+\s*(?:-|to)\s*(\$|₹|€)?[0-9,]+", text)
    if match:
        return match.group(0)
    return None


def extract_qualifications(text: str) -> List[str]:
    """Extract qualifications from JD"""
    qualifications = []
    if any(q in text.lower() for q in ["bachelor", "master", "degree", "certification"]):
        qualifications = ["Bachelor's Degree", "Relevant Experience"]
    return qualifications


def extract_responsibilities(text: str) -> List[str]:
    """Extract responsibilities from JD"""
    responsibilities = []
    # Look for bullet points or numbered lists
    lines = text.split("\n")
    for line in lines:
        if line.strip().startswith(("•", "-", "*", "•", "1.", "2.", "3.")):
            resp = line.strip().lstrip("•-*123456789. ").strip()
            if resp and len(resp) > 10:
                responsibilities.append(resp)
    # Limit to first 5 responsibilities
    return responsibilities[:5] if responsibilities else ["Responsibilities not clearly defined"]
