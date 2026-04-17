#!/usr/bin/env python3
"""Diagnostic script to check backend database config"""
import os
import sys
sys.path.insert(0, 'backend')

from dotenv import load_dotenv
from backend.db.connection import SessionLocal
from backend.models.user import User
from backend.services.auth import verify_password

load_dotenv()

print("=" * 60)
print("Backend Database Diagnostic")
print("=" * 60)

try:
    db = SessionLocal()
    
    # Check if user exists
    user = db.query(User).filter(User.email == "rishigupta9711@gmail.com").first()
    
    if user:
        print(f"\n✅ User found in backend database:")
        print(f"   Email: {user.email}")
        print(f"   Role: {user.role}")
        print(f"   ID: {user.id}")
        print(f"   Hashed Password (first 20 chars): {user.hashed_password[:20]}...")
        
        # Test password verification
        password = "rishi@9711"
        is_valid = verify_password(password, user.hashed_password)
        print(f"\n   Password verification for '{password}':")
        print(f"   Result: {'✅ VALID' if is_valid else '❌ INVALID'}")
        
        # Try with different variations
        test_passwords = [
            "rishi@9711",
            "rishi@9711 ",
            " rishi@9711",
            "rishi@9711\n",
            "Rishi@9711"
        ]
        
        print(f"\n   Testing password variations:")
        for pwd in test_passwords:
            try:
                result = verify_password(pwd, user.hashed_password)
                print(f"      '{pwd}' -> {result}")
            except:
                print(f"      '{pwd}' -> ERROR")
    else:
        print(f"\n❌ User NOT found in backend database!")
        print(f"   Email searched: rishigupta9711@gmail.com")
        print(f"   Checking all admins...")
        
        admins = db.query(User).filter(User.role == "admin").all()
        if admins:
            print(f"   Found {len(admins)} admins:")
            for admin in admins:
                print(f"      - {admin.email}")
        else:
            print(f"   No admins found!")
    
    db.close()
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
