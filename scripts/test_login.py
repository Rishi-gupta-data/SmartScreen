#!/usr/bin/env python3
"""Test login endpoint directly"""
import requests
import json

try:
    url = "http://localhost:8000/api/v1/auth/login"
    payload = {
        "email": "rishigupta9711@gmail.com",
        "password": "rishi@9711"
    }
    
    print(f"Testing login endpoint...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(url, json=payload, timeout=5)
    
    print(f"\nResponse Status: {response.status_code}")
    print(f"Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        print("\n✅ Login successful!")
        print(f"Token: {response.json().get('access_token', '')[:50]}...")
    else:
        print(f"\n❌ Login failed with status {response.status_code}")
        
except requests.exceptions.ConnectionError as e:
    print(f"❌ Connection Error: Backend not running on http://localhost:8000")
    print(f"   Make sure the backend server is started:")
    print(f"   cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
except Exception as e:
    print(f"❌ Error: {e}")
