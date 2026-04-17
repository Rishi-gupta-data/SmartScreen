#!/usr/bin/env python3
"""Check which databases are being used"""
import os
import sys

sys.path.insert(0, 'backend')

from dotenv import load_dotenv
from backend.db.connection import DATABASE_URL as BACKEND_DB_URL
from backend.config import settings

load_dotenv()
env_db = os.getenv("DATABASE_URL", "sqlite:///./smartscreen.db")

print("=" * 60)
print("Database URL Configuration Check")
print("=" * 60)

print(f"\nEnvironment Variable (DATABASE_URL):")
print(f"  {env_db[:60]}...")

print(f"\nBackend Using:")
print(f"  {BACKEND_DB_URL}")

print(f"\nAPI Settings:")
print(f"  Environment: {settings.environment}")

if BACKEND_DB_URL.startswith("sqlite"):
    print(f"\n⚠️  Backend is using SQLite (local file)")
    print(f"   Seed script created admin in PostgreSQL/Neon")
    print(f"   SOLUTION: Restart backend to reload environment, or update .env to use SQLite")
else:
    print(f"\n✅ Both using PostgreSQL")
