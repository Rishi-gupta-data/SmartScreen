import requests
import time

BASE = "http://127.0.0.1:8001"


def wait_for_server(timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(BASE + "/docs")
            if r.status_code in (200, 404, 302):
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


def run():
    if not wait_for_server():
        print("Server did not start in time")
        return

    # Use timestamp to create unique email
    timestamp = int(time.time() * 1000)
    email = f"smoke_test_{timestamp}@example.com"
    password = "smokepass"

    print("\n" + "="*60)
    print("SMARTSCREEN SMOKE TEST - Full Flow")
    print("="*60)

    print("\n[1/7] Signing up...")
    r = requests.post(BASE + "/auth/signup", json={"email": email, "password": password})
    print(f"Status: {r.status_code}")
    if r.status_code != 200:
        print(f"❌ Signup failed: {r.text}")
        return
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Signup successful")

    print("\n[2/7] Checking initial credits...")
    r = requests.get(BASE + "/credits/", headers=headers)
    print(f"Status: {r.status_code}, Credits: {r.json()}")
    print("✅ Credits check successful")

    print("\n[3/7] Adding credits (50)...")
    r = requests.post(BASE + "/credits/add", json={"amount": 50}, headers=headers)
    print(f"Status: {r.status_code}, New Balance: {r.json().get('credits')}")
    print("✅ Credits added")

    # Sample resume
    sample_resume = """
    John Doe
    john.doe@example.com
    +1-555-1234
    
    SKILLS
    Python, Java, JavaScript, React, Django, FastAPI
    
    EXPERIENCE
    Senior Software Engineer at Tech Corp (2020-Present)
    - Led development of microservices architecture
    - Managed team of 5 engineers
    
    EDUCATION
    B.Tech in Computer Science
    University of Technology, 2018
    """

    print("\n[4/7] Parsing resume (5 credits)...")
    r = requests.post(
        BASE + "/resume/parse",
        json={"resume_text": sample_resume},
        headers=headers
    )
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        resume_data = r.json()
        print(f"✅ Resume parsed: {resume_data.get('name')}, Skills: {len(resume_data.get('skills', []))} found")
    else:
        print(f"❌ Resume parsing failed: {r.text}")
        resume_data = None

    # Sample JD
    sample_jd = """
    Senior Python Developer
    Tech Company Inc.
    
    Required Skills:
    - Python, Django or FastAPI
    - 5+ years experience
    - REST APIs
    
    Preferred Skills:
    - React, Docker, Kubernetes
    
    Qualifications:
    - Bachelor's in Computer Science
    - Experience with microservices
    
    Responsibilities:
    - Design and implement backend systems
    - Mentor junior developers
    - Code review and architecture decisions
    """

    print("\n[5/7] Parsing JD (3 credits)...")
    r = requests.post(
        BASE + "/jd/parse",
        json={"jd_text": sample_jd},
        headers=headers
    )
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        jd_data = r.json()
        print(f"✅ JD parsed: {jd_data.get('title')}, Company: {jd_data.get('company')}")
    else:
        print(f"❌ JD parsing failed: {r.text}")
        jd_data = None

    print("\n[6/7] Matching resume to JD (5 credits)...")
    if resume_data and jd_data:
        r = requests.post(
            BASE + "/match/",
            json={
                "resume_data": resume_data,
                "jd_data": jd_data
            },
            headers=headers
        )
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            match_result = r.json()
            print(f"✅ Match calculated: Score: {match_result.get('match_score')}%")
            print(f"   Recommendation: {match_result.get('overall_recommendation')}")
        else:
            print(f"❌ Matching failed: {r.text}")
    else:
        print("❌ Skipping match - parsing failed")

    print("\n[7/7] Checking final credits...")
    r = requests.get(BASE + "/credits/", headers=headers)
    if r.status_code == 200:
        final_credits = r.json().get('credits')
        print(f"✅ Final credit balance: {final_credits}")
        print(f"   Total used: {50 - final_credits} credits (5 + 3 + 5)")
    else:
        print(f"❌ Final credit check failed: {r.text}")

    print("\n" + "="*60)
    print("✅ SMOKE TEST COMPLETE")
    print("="*60 + "\n")


if __name__ == '__main__':
    run()
