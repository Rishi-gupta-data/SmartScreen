#!/usr/bin/env python3
"""
Script to create initial admin account for SmartScreen.
Run this once to set up the first admin.

Usage:
    python create_admin_seed.py
"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from sqlalchemy.orm import Session
from backend.db.connection import engine, Base, SessionLocal
from backend.models.user import User
from backend.services.auth import get_password_hash


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")


def seed_admin(email: str, password: str):
    """Create an admin user"""
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"❌ Admin with email '{email}' already exists")
            return False
        
        # Create admin
        hashed_password = get_password_hash(password)
        admin = User(
            email=email,
            hashed_password=hashed_password,
            role="admin",
            credits=0
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print(f"✅ Admin created successfully!")
        print(f"   Email: {email}")
        print(f"   Role: admin")
        print(f"   ID: {admin.id}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def main():
    """Main entry point"""
    print("=" * 50)
    print("SmartScreen Admin Account Seed")
    print("=" * 50)
    
    # Create tables first
    create_tables()
    
    print("\n📝 Creating Admin Account...")
    print("-" * 50)
    
    # Get admin credentials from user
    while True:
        email = input("Enter admin email: ").strip()
        if "@" not in email:
            print("❌ Please enter a valid email address")
            continue
        break
    
    while True:
        password = input("Enter admin password (min 6 characters): ").strip()
        if len(password) < 6:
            print("❌ Password must be at least 6 characters")
            continue
        
        confirm_password = input("Confirm password: ").strip()
        if password != confirm_password:
            print("❌ Passwords don't match")
            continue
        break
    
    # Create admin
    if seed_admin(email, password):
        print("\n" + "=" * 50)
        print("✅ Setup Complete!")
        print("=" * 50)
        print(f"\nYou can now login with:")
        print(f"  Email: {email}")
        print(f"  Password: ••••••••")
        print("\nAccess Admin Panel at: http://localhost:3000/admin-login")
    else:
        print("\n❌ Failed to create admin account")
        sys.exit(1)


if __name__ == "__main__":
    main()
