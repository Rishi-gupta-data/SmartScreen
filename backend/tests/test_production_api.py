"""
Production API Testing Suite for SmartScreen
Tests all endpoints to ensure production readiness
"""

import requests
import json
import sys
from typing import Dict, Any, Optional
import time

# Configuration
BASE_URL = "http://localhost:8000"  # Change to production URL
TEST_USER_EMAIL = f"testuser-{int(time.time())}@test.com"
TEST_USER_PASSWORD = "TestPass123!"

# ANSI Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
END = '\033[0m'

# Global variables
access_token: Optional[str] = None
user_id: Optional[str] = None
resume_text = """
John Doe
john.doe@example.com | +91-9876543210 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced Backend Engineer with 5+ years in Python and FastAPI development.

TECHNICAL SKILLS
Python, JavaScript, FastAPI, Django, PostgreSQL, MongoDB, Docker, Kubernetes, AWS, Redis

PROFESSIONAL EXPERIENCE
Senior Backend Engineer | TechCorp Inc. | Jan 2022 – Present
- Designed and implemented FastAPI microservices
- Optimized PostgreSQL queries, improved performance by 40%
- Managed Docker containers and Kubernetes deployments

Backend Engineer | StartupXYZ | Jun 2019 – Dec 2021
- Built REST APIs using Python and FastAPI
- Implemented MongoDB solutions
- Contributed to DevOps improvements

EDUCATION
B.Tech in Computer Science | Delhi Tech University | 2019
"""

jd_text = """
Senior Backend Engineer

ABOUT THE ROLE
We're looking for an experienced Backend Engineer to join our team.

REQUIREMENTS
Experience: 5+ years in backend development
Required Skills:
- Python (mandatory)
- FastAPI or Django (mandatory)
- PostgreSQL (mandatory)
- Docker (mandatory)
- Kubernetes (mandatory)

Preferred Skills:
- Redis
- Microservices architecture

QUALIFICATIONS
- Bachelor's degree in Computer Science
- 5+ years of professional backend development experience
"""


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{BLUE}{'='*80}{END}")
    print(f"{BLUE}{text:^80}{END}")
    print(f"{BLUE}{'='*80}{END}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✅ {text}{END}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}❌ {text}{END}")


def print_info(text: str):
    """Print info message."""
    print(f"{BLUE}ℹ️  {text}{END}")


def print_test(test_name: str):
    """Print test name."""
    print(f"\n{YELLOW}▶️  {test_name}{END}")


def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    expected_status: int = 200,
) -> tuple[bool, Any]:
    """Make HTTP request and validate response."""
    
    url = f"{BASE_URL}{endpoint}"
    
    if headers is None:
        headers = {"Content-Type": "application/json"}
    
    if access_token and "Authorization" not in headers:
        headers["Authorization"] = f"Bearer {access_token}"
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            print_error(f"Unknown method: {method}")
            return False, None
        
        if response.status_code == expected_status:
            print_success(f"{method} {endpoint} → {response.status_code}")
            return True, response.json() if response.text else {}
        else:
            print_error(
                f"{method} {endpoint} → {response.status_code} "
                f"(expected {expected_status})\n"
                f"Response: {response.text[:200]}"
            )
            return False, response.json() if response.text else {}
    
    except requests.exceptions.ConnectionError:
        print_error(f"Connection failed to {url}")
        return False, None
    except Exception as e:
        print_error(f"Request failed: {e}")
        return False, None


# ═══════════════════════════════════════════════════════════════════════════
# TEST SUITE
# ═══════════════════════════════════════════════════════════════════════════

def test_health():
    """Test health endpoint."""
    print_test("Health Check")
    success, response = make_request("GET", "/health", expected_status=200)
    
    if success:
        print_info(f"Health response: {response}")
    
    return success


def test_root():
    """Test root endpoint."""
    print_test("Root Endpoint")
    success, response = make_request("GET", "/", expected_status=200)
    
    if success:
        print_info(f"Root response: {json.dumps(response, indent=2)}")
    
    return success


def test_signup():
    """Test user signup."""
    global access_token, user_id
    print_test("User Signup")
    
    payload = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    success, response = make_request(
    "POST", "/auth/signup", data=payload, expected_status=200
    )
    
    if success:
        user_id = response.get("id")
        print_info(f"User created: {TEST_USER_EMAIL} (ID: {user_id})")
        print_info(f"Initial credits: {response.get('credits')}")
    
    return success


def test_login():
    """Test user login."""
    global access_token
    print_test("User Login")
    
    payload = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    success, response = make_request(
    "POST", "/auth/login", data=payload, expected_status=200
    )
    
    if success:
        access_token = response.get("access_token")
        print_info(f"Token obtained: {access_token[:50]}...")
    
    return success


def test_get_credits():
    """Test get credits endpoint."""
    print_test("Get Credits Balance")
    
    success, response = make_request("GET", "/credits/", expected_status=200)    
    
    if success:
        print_info(f"Credits: {response.get('credits')}")
        print_info(f"User ID: {response.get('user_id')}")
    
    return success


def test_parse_resume():
    """Test resume parsing."""
    print_test("Parse Resume")
    
    payload = {"resume_text": resume_text}
    
    success, response = make_request(
    "POST", "/resume/parse", data=payload, expected_status=200
    )
    
    if success:
        print_info(f"Name: {response.get('name')}")
        print_info(f"Email: {response.get('email')}")
        print_info(f"Phone: {response.get('phone')}")
        print_info(f"Skills: {', '.join(response.get('skills', [])[:5])}...")
        print_info(f"Experience: {response.get('total_experience_years')} years")
        print_info(f"Education: {response.get('education')}")
        print_info(f"Credits deducted: {response.get('credits_deducted')}")
    
    return success


def test_parse_jd():
    """Test JD parsing."""
    print_test("Parse Job Description")
    
    payload = {"jd_text": jd_text}
    
    success, response = make_request(
    "POST", "/jd/parse", data=payload, expected_status=200
    )
    
    if success:
        print_info(f"Job Title: {response.get('title')}")
        print_info(f"Company: {response.get('company')}")
        print_info(f"Required Skills: {', '.join(response.get('required_skills', [])[:5])}...")
        print_info(f"Experience Required: {response.get('experience_required')}")
        print_info(f"Credits deducted: {response.get('credits_deducted')}")
    
    return success


def test_match():
    """Test resume-to-JD matching."""
    print_test("Match Resume to Job Description")
    
    payload = {
        "resume_text": resume_text,
        "jd_text": jd_text
    }
    
    success, response = make_request("POST", "/match/", data=payload, expected_status=200)
    
    if success:
        print_info(f"Match Score: {response.get('match_score')}/100")
        breakdown = response.get('breakdown', {})
        print_info(f"  Skill Score: {breakdown.get('skill_score')}/100 - {breakdown.get('skill_score_detail')}")
        print_info(f"  Experience: {breakdown.get('experience_score')}/100 - {breakdown.get('experience_score_detail')}")
        print_info(f"  Education: {breakdown.get('education_score')}/100 - {breakdown.get('education_score_detail')}")
        
        fitment = response.get('fitment_category', {})
        print_info(f"Fitment: {fitment.get('emoji')} {fitment.get('label')}")
        
        print_info(f"Improvement Tips:")
        for i, tip in enumerate(response.get('improvement_tips', []), 1):
            print_info(f"  {i}. {tip}")
        
        print_info(f"Credits deducted: {response.get('credits_deducted')}")
    
    return success


def test_get_transactions():
    """Test get transactions."""
    print_test("Get Transactions")
    
    success, response = make_request(
    "GET", "/billing/transactions", expected_status=200)
    
    if success:
        transactions = response.get('transactions', [])
        print_info(f"Total transactions: {len(transactions)}")
        for tx in transactions[:3]:
            print_info(f"  {tx.get('type')}: {tx.get('amount')} credits - {tx.get('description')}")
    
    return success


def run_all_tests():
    """Run all tests in sequence."""
    print_header("SmartScreen API Production Test Suite")
    
    print_info(f"Base URL: {BASE_URL}")
    print_info(f"Test User: {TEST_USER_EMAIL}\n")
    
    tests = [
        ("Health Check", test_health),
        ("Root Endpoint", test_root),
        ("User Registration", test_signup),
        ("User Login", test_login),
        ("Get Credits", test_get_credits),
        ("Parse Resume", test_parse_resume),
        ("Parse Job Description", test_parse_jd),
        ("Resume-to-JD Matching", test_match),
        ("Get Transactions", test_get_transactions),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{END}" if result else f"{RED}FAIL{END}"
        print(f"  {status} - {test_name}")
    
    print(f"\n{BLUE}Total: {passed}/{total} tests passed{END}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 All tests passed! API is production-ready!{END}\n")
        return 0
    else:
        print(f"\n{RED}⚠️  Some tests failed. Check configuration.{END}\n")
        return 1


if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Tests interrupted by user{END}")
        sys.exit(1)
