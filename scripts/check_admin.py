#!/usr/bin/env python3
"""Check if admin account exists in database"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT email, role FROM users WHERE role='admin' LIMIT 5"))
        admins = result.fetchall()
        if admins:
            print('✅ Found admins in database:')
            for admin in admins:
                print(f'   Email: {admin[0]}, Role: {admin[1]}')
        else:
            print('❌ No admins found in database')
except Exception as e:
    print(f'❌ Database error: {e}')
