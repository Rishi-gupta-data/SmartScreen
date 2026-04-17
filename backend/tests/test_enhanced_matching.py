"""
Test enhanced parsing and matching capabilities.
Tests cover: resume parsing, JD parsing, and intelligent matching.
"""

import sys
import json
import os
import importlib.util

# Load parsing_service directly without going through __init__.py
spec = importlib.util.spec_from_file_location(
    "parsing_service",
    os.path.join(os.path.dirname(__file__), '..', 'services', 'parsing_service.py')
)
parsing_service = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parsing_service)

# ═══════════════════════════════════════════════════════════════════════════
# TEST CASE 1: Strong Match (85%+)
# ═══════════════════════════════════════════════════════════════════════════

RESUME_1 = """
JOHN SMITH
john.smith@email.com | +91-9876543210 | linkedin.com/in/johnsmith | github.com/johnsmith

PROFESSIONAL SUMMARY
Experienced Backend Engineer with 5+ years in Python and FastAPI development.

TECHNICAL SKILLS
Languages: Python, JavaScript, SQL, Bash
Backend: FastAPI, Django, REST APIs, Microservices
Databases: PostgreSQL, MongoDB, Redis
DevOps: Docker, Kubernetes, AWS EC2, AWS RDS, AWS S3
Other: Git, GitHub, Jira, Linux

PROFESSIONAL EXPERIENCE
Senior Backend Engineer | TechCorp Inc. | Jan 2022 – Present (1+ years)
- Designed and implemented FastAPI microservices handling 10K+ requests/day
- Optimized PostgreSQL queries, improved performance by 40%
- Managed Docker containers and Kubernetes deployments on AWS

Backend Engineer | StartupXYZ | Jun 2019 – Dec 2021 (2+ years)
- Built REST APIs using Python and FastAPI framework
- Implemented MongoDB solutions for document management
- Contributed to DevOps improvements using Docker and Kubernetes

Junior Backend Engineer | WebServices Ltd. | Aug 2018 – May 2019 (1 year)
- Developed Python web services
- Participated in code reviews and testing

EDUCATION
B.Tech in Computer Science | Delhi Institute of Technology | 2018
"""

JOB_DESCRIPTION_1 = """
Senior Backend Engineer

ABOUT THE ROLE
We're looking for an experienced Backend Engineer to join our growing team.

REQUIREMENTS
Experience: 5+ years in backend development
Required Skills:
- Python (mandatory)
- FastAPI or Django (mandatory)
- PostgreSQL (mandatory)
- Docker (mandatory)
- Kubernetes (mandatory)
- AWS (mandatory)

Preferred Skills:
- Redis
- Microservices architecture
- RESTful API design

QUALIFICATIONS
- Bachelor's degree in Computer Science or related field
- 5+ years of professional backend development experience
- Strong understanding of database design

RESPONSIBILITIES
- Design and implement scalable backend services
- Optimize database performance
- Lead technical discussions
- Mentor junior developers
"""

# ═══════════════════════════════════════════════════════════════════════════
# TEST CASE 2: Medium Match (60-75%)
# ═══════════════════════════════════════════════════════════════════════════

RESUME_2 = """
SARAH KHAN
sarah.khan@email.com | +91-9876543211

TECHNICAL SKILLS
Languages: Python, JavaScript
Backend: Django, Flask
Databases: MySQL, PostgreSQL
DevOps: Docker
Other: Git

PROFESSIONAL EXPERIENCE
Backend Developer | E-Commerce Co. | Jan 2021 – Present (2 years)
- Developed Django web applications
- Wrote SQL queries for MySQL and PostgreSQL
- Managed Docker containers for deployment
- Basic AWS usage (EC2 instances)

Junior Developer | Web Agency | Jun 2019 – Dec 2020 (1.5 years)
- Built Python web applications
- Worked with relational databases

EDUCATION
B.Com with IT | Mumbai University | 2019
"""

JOB_DESCRIPTION_2 = """
Backend Developer (Python + FastAPI)

Required Skills:
- Python
- FastAPI
- PostgreSQL
- Docker
- REST APIs

Preferred Skills:
- JavaScript
- Kubernetes
- React (for frontend collaboration)

Experience Required: 3-4 years
Education: Bachelor's degree
"""

# ═══════════════════════════════════════════════════════════════════════════
# TEST CASE 3: Weak Match (30-50%)
# ═══════════════════════════════════════════════════════════════════════════

RESUME_3 = """
ALEX PATEL
alex.patel@email.com

TECHNICAL SKILLS
Languages: Java, Python
Other: HTML, CSS, Bootstrap

PROFESSIONAL EXPERIENCE
Junior Web Developer | Design Studio | Jun 2023 – Present (6 months)
- HTML, CSS, JavaScript for web pages
- Basic Python scripts

EDUCATION
Bachelor's in IT | Unknown College | 2023
"""

JOB_DESCRIPTION_3 = """
Senior Backend Engineer - Microservices

Required Skills:
- Python
- FastAPI
- Docker
- Kubernetes
- AWS
- PostgreSQL
- Redis

Experience Required: 7+ years
Education: Bachelor's degree in CS
"""


def test_case(name: str, resume_text: str, jd_text: str):
    """Run a single test case."""
    print(f"\n{'='*80}")
    print(f"TEST: {name}")
    print(f"{'='*80}\n")
    
    # Parse resume
    print("📄 PARSING RESUME...")
    resume = parsing_service.parse_resume(resume_text)
    print(f"  Name: {resume.get('name')}")
    print(f"  Experience: {resume.get('total_experience_years')} years ({resume.get('experience_level')})")
    print(f"  Skills ({len(resume.get('skills', []))}): {', '.join(resume.get('skills', [])[:8])}")
    print(f"  Education: {resume.get('education')}\n")
    
    # Parse JD
    print("💼 PARSING JOB DESCRIPTION...")
    jd = parsing_service.parse_jd(jd_text)
    print(f"  Title: {jd.get('title')}")
    print(f"  Company: {jd.get('company')}")
    print(f"  Required Skills: {', '.join(jd.get('required_skills', []))}")
    print(f"  Preferred Skills: {', '.join(jd.get('preferred_skills', []))}")
    print(f"  Experience Required: {jd.get('experience_required')}")
    print(f"  Qualifications: {', '.join(jd.get('qualifications', []))}\n")
    
    # Match
    print("🔍 MATCHING RESUME TO JOB...")
    match = parsing_service.match_resume_to_jd(resume, jd)
    
    # Print results
    print(f"\n📊 MATCH SCORE: {match['match_score']}/100")
    print(f"   Category: {match['fitment_category']['emoji']} {match['fitment_category']['label']}")
    print(f"   Description: {match['fitment_category']['description']}\n")
    
    print("📈 DETAILED BREAKDOWN:")
    breakdown = match['breakdown']
    print(f"   Skills:      {breakdown['skill_score']}/100")
    print(f"                {breakdown['skill_score_detail']}")
    print(f"   Experience: {breakdown['experience_score']}/100")
    print(f"                {breakdown['experience_score_detail']}")
    print(f"   Education:  {breakdown['education_score']}/100")
    print(f"                {breakdown['education_score_detail']}\n")
    
    print("🎯 SKILL ANALYSIS:")
    skill_match = match['skill_match']
    print(f"   Required Matched:  {', '.join(skill_match['required_matched']) if skill_match['required_matched'] else 'None'}")
    print(f"   Required Missing:  {', '.join(skill_match['required_missing']) if skill_match['required_missing'] else 'None'}")
    print(f"   Preferred Matched: {', '.join(skill_match['preferred_matched']) if skill_match['preferred_matched'] else 'None'}")
    print(f"   Preferred Missing: {', '.join(skill_match['preferred_missing']) if skill_match['preferred_missing'] else 'None'}")
    print(f"   Extra Skills:      {', '.join(skill_match['extra_skills']) if skill_match['extra_skills'] else 'None'}\n")
    
    print("💬 RECOMMENDATION:")
    print(f"   {match['overall_recommendation']}")
    print(f"   {match['recommendation_detail']}\n")
    
    print("💡 IMPROVEMENT TIPS:")
    for i, tip in enumerate(match['improvement_tips'], 1):
        print(f"   {i}. {tip}\n")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("ENHANCED PARSING & MATCHING TEST SUITE")
    print("="*80)
    
    # Run test cases
    test_case("Strong Match (85%+)", RESUME_1, JOB_DESCRIPTION_1)
    test_case("Medium Match (60-75%)", RESUME_2, JOB_DESCRIPTION_2)
    test_case("Weak Match (30-50%)", RESUME_3, JOB_DESCRIPTION_3)
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80 + "\n")
