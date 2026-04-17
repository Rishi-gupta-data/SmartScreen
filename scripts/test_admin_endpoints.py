#!/usr/bin/env python3
"""
Test script for SmartScreen Admin Panel endpoints.
Tests all admin CRUD operations and validates responses.

Usage:
    python test_admin_endpoints.py
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

# Test data
TEST_ADMIN_EMAIL = f"test_admin_{int(datetime.now().timestamp())}@test.com"
TEST_ADMIN_PASSWORD = "TestPassword123"
TEST_UPDATE_EMAIL = f"updated_admin_{int(datetime.now().timestamp())}@test.com"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

# Track test results
tests_passed = 0
tests_failed = 0
admin_token = None
created_admin_id = None


def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}\n")


def print_success(text):
    """Print success message"""
    global tests_passed
    tests_passed += 1
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")


def print_error(text):
    """Print error message"""
    global tests_failed
    tests_failed += 1
    print(f"{Colors.RED}❌ {text}{Colors.END}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.YELLOW}ℹ️  {text}{Colors.END}")


def print_response(response, title="Response"):
    """Print response details"""
    print(f"\n{Colors.YELLOW}{title}:{Colors.END}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)


def test_admin_login(email, password):
    """Test admin login and get JWT token"""
    global admin_token
    
    print_header("TEST 1: Admin Login (Get JWT Token)")
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/auth/login"
        payload = {"email": email, "password": password}
        
        print_info(f"POST {url}")
        print_info(f"Payload: {payload}")
        
        response = requests.post(url, json=payload)
        print_response(response)
        
        if response.status_code == 200:
            admin_token = response.json()["access_token"]
            print_success(f"Login successful. Token received: {admin_token[:20]}...")
            return True
        else:
            print_error(f"Login failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Login error: {str(e)}")
        return False


def get_headers():
    """Get authorization headers"""
    if not admin_token:
        print_error("No admin token available")
        return None
    return {"Authorization": f"Bearer {admin_token}"}


def test_get_admin_stats():
    """Test GET /admin/stats"""
    print_header("TEST 2: Get Admin Stats")
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/stats"
        headers = get_headers()
        
        print_info(f"GET {url}")
        
        response = requests.get(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Stats retrieved: {data.get('total_users')} users, {data.get('total_admins')} admins")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_list_admins():
    """Test GET /admin/list"""
    print_header("TEST 3: List All Admins")
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/list"
        headers = get_headers()
        
        print_info(f"GET {url}")
        
        response = requests.get(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            admins = response.json()
            print_success(f"Listed {len(admins)} admin(s)")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_create_admin():
    """Test POST /admin/create"""
    global created_admin_id
    
    print_header("TEST 4: Create New Admin")
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/create"
        headers = get_headers()
        payload = {"email": TEST_ADMIN_EMAIL, "password": TEST_ADMIN_PASSWORD}
        
        print_info(f"POST {url}")
        print_info(f"Payload: {payload}")
        
        response = requests.post(url, json=payload, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            created_admin_id = data.get("id")
            print_success(f"Admin created with ID: {created_admin_id}")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_get_specific_admin():
    """Test GET /admin/{id}"""
    print_header("TEST 5: Get Specific Admin Details")
    
    if not created_admin_id:
        print_info("Skipping - No created admin ID")
        return False
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/{created_admin_id}"
        headers = get_headers()
        
        print_info(f"GET {url}")
        
        response = requests.get(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Admin retrieved: {data.get('email')}")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_update_admin():
    """Test PUT /admin/{id}"""
    print_header("TEST 6: Update Admin Details")
    
    if not created_admin_id:
        print_info("Skipping - No created admin ID")
        return False
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/{created_admin_id}"
        headers = get_headers()
        payload = {"email": TEST_UPDATE_EMAIL, "password": "UpdatedPassword456"}
        
        print_info(f"PUT {url}")
        print_info(f"Payload: {payload}")
        
        response = requests.put(url, json=payload, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Admin updated: {data.get('email')}")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_list_admins_verify_update():
    """Test GET /admin/list to verify update"""
    print_header("TEST 7: Verify Admin List After Update")
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/list"
        headers = get_headers()
        
        print_info(f"GET {url}")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            admins = response.json()
            # Check if updated admin is in list
            for admin in admins:
                if admin.get("email") == TEST_UPDATE_EMAIL:
                    print_success(f"Updated admin found in list: {admin.get('email')}")
                    return True
            print_error("Updated admin not found in list")
            return False
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_delete_admin():
    """Test DELETE /admin/{id}"""
    print_header("TEST 8: Delete Admin")
    
    if not created_admin_id:
        print_info("Skipping - No created admin ID")
        return False
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/{created_admin_id}"
        headers = get_headers()
        
        print_info(f"DELETE {url}")
        
        response = requests.delete(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            print_success("Admin deleted successfully")
            return True
        else:
            print_error(f"Failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_verify_deletion():
    """Test GET /admin/{id} to verify deletion"""
    print_header("TEST 9: Verify Admin Deletion")
    
    if not created_admin_id:
        print_info("Skipping - No created admin ID")
        return False
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/{created_admin_id}"
        headers = get_headers()
        
        print_info(f"GET {url}")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 404:
            print_success("Admin successfully deleted (404 not found)")
            return True
        else:
            print_error(f"Admin still exists or unexpected status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_unauthorized_access():
    """Test unauthorized access without token"""
    print_header("TEST 10: Test Unauthorized Access (No Token)")
    
    try:
        url = f"{BASE_URL}{API_PREFIX}/admin/stats"
        
        print_info(f"GET {url} (without token)")
        
        response = requests.get(url)
        
        if response.status_code == 401 or response.status_code == 403:
            print_success(f"Correctly rejected unauthorized access (status {response.status_code})")
            return True
        else:
            print_error(f"Unexpected status {response.status_code} (expected 401/403)")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print_header("SmartScreen Admin Panel - API Tests")
    print_info("Starting admin endpoint tests...")
    print_info(f"Base URL: {BASE_URL}")
    
    # Check if backend is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print_error(f"Backend not responding correctly (status: {response.status_code})")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend. Make sure it's running on port 8000")
        sys.exit(1)
    
    print_success("Backend is running")
    
    # Run tests (you need an existing admin account to login first)
    print("\n" + Colors.YELLOW + "Note: You need existing admin credentials to run these tests" + Colors.END)
    admin_email = input(f"{Colors.BLUE}Enter existing admin email: {Colors.END}").strip()
    admin_password = input(f"{Colors.BLUE}Enter admin password: {Colors.END}").strip()
    
    if not test_admin_login(admin_email, admin_password):
        print_error("Cannot proceed without valid admin login")
        sys.exit(1)
    
    # Run all tests
    test_get_admin_stats()
    test_list_admins()
    test_create_admin()
    test_get_specific_admin()
    test_update_admin()
    test_list_admins_verify_update()
    test_delete_admin()
    test_verify_deletion()
    test_unauthorized_access()
    
    # Print summary
    print_header("Test Summary")
    total_tests = tests_passed + tests_failed
    print(f"Total Tests: {total_tests}")
    print(f"{Colors.GREEN}Passed: {tests_passed}{Colors.END}")
    print(f"{Colors.RED}Failed: {tests_failed}{Colors.END}")
    
    if tests_failed == 0:
        print(f"\n{Colors.GREEN}All tests passed! ✅{Colors.END}")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}Some tests failed! ❌{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()
