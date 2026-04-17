#!/usr/bin/env python3
"""
🔧 SmartScreen Startup Fix - Interactive Guide
Fixes the ModuleNotFoundError: No module named 'backend'
"""

import os
import sys
import subprocess
from pathlib import Path

print("\n" + "=" * 80)
print("🔧 SmartScreen Startup Troubleshooting")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════════
# ROOT CAUSE ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════
print("""
❌ PROBLEM:
ModuleNotFoundError: No module named 'backend'

🔍 ROOT CAUSE:
You're running uvicorn from the 'backend' directory:
  cd C:\\Users\\RishiGupta\\SmartScreen\\backend
  python -m uvicorn backend.main:app --reload --port 8000

When Python runs from INSIDE 'backend/', it can't find:
  - from backend.db.connection import engine, Base
  - from backend.config import settings
  - from backend.routes import auth_router, ...

Because the 'backend' module is not importable from within itself.

✅ SOLUTION:
Always run uvicorn from the SmartScreen ROOT directory, not from backend/

The Python path needs to include SmartScreen root so it can find 'backend' package.
""")

# ═══════════════════════════════════════════════════════════════════════════
# STEP BY STEP FIX
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("📋 STEP-BY-STEP FIX")
print("=" * 80)

root_dir = Path("C:\\Users\\RishiGupta\\SmartScreen")
backend_dir = root_dir / "backend"
env_file = root_dir / ".env"

# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 1: Verify you're in correct directory")
print("─" * 80)

current_dir = Path.cwd()
print(f"Current directory: {current_dir}")

if current_dir == backend_dir:
    print("❌ You're in the backend directory (WRONG)")
    print(f"✅ Fix: cd {root_dir}")
    os.chdir(root_dir)
    print(f"Changed to: {Path.cwd()}")
elif current_dir == root_dir:
    print("✅ You're in the root directory (CORRECT)")
else:
    print(f"⚠️  You're in: {current_dir}")
    print(f"✅ Should be: {root_dir}")

# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 2: Verify .env file exists and is configured")
print("─" * 80)

if env_file.exists():
    print(f"✅ .env file exists: {env_file}")
    
    # Check if DATABASE_URL is set
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
            has_db = 'DATABASE_URL' in content
            has_secret = 'SECRET_KEY' in content
            
            print(f"   DATABASE_URL configured: {'✅' if has_db else '❌'}")
            print(f"   SECRET_KEY configured: {'✅' if has_secret else '❌'}")
            
            if not has_db:
                print("\n⚠️  DATABASE_URL not set!")
                print("   Add to .env: DATABASE_URL=postgresql://user:pass@host/db")
            if not has_secret:
                print("\n⚠️  SECRET_KEY not set!")
                print("   Add to .env: SECRET_KEY=<random-32-char-string>")
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
else:
    print(f"❌ .env file not found!")
    print(f"✅ Fix: copy .env.example .env")

# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 3: Verify backend folder structure")
print("─" * 80)

required_dirs = ['backend/db', 'backend/models', 'backend/routes', 'backend/services', 'backend/tests']
required_files = ['backend/__init__.py', 'backend/main.py', 'backend/config.py']

print("Required directories:")
for d in required_dirs:
    path = root_dir / d
    status = "✅" if path.exists() else "❌"
    print(f"  {status} {d}")

print("\nRequired files:")
for f in required_files:
    path = root_dir / f
    status = "✅" if path.exists() else "❌"
    print(f"  {status} {f}")

# ─────────────────────────────────────────────────────────────────────────────
print("\nSTEP 4: Verify Python dependencies")
print("─" * 80)

required_packages = ['fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 'python_jose']
missing = []

for pkg in required_packages:
    try:
        __import__(pkg.replace('-', '_'))
        print(f"  ✅ {pkg}")
    except ImportError:
        print(f"  ❌ {pkg} (MISSING)")
        missing.append(pkg)

if missing:
    print(f"\n⚠️  Missing: {', '.join(missing)}")
    print("✅ Fix: pip install -r requirements-prod.txt")

# ═══════════════════════════════════════════════════════════════════════════
# CORRECT COMMAND
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("✅ COMMANDS TO RUN (FROM THIS DIRECTORY):")
print("=" * 80)

print(f"""
# Make sure you're in the root directory:
cd C:\\Users\\RishiGupta\\SmartScreen

# 1. Initialize database (one time only)
python -c "from backend.create_tables import create_schema; create_schema()"

# 2. Start the API server (Terminal 1)
python -m uvicorn backend.main:app --reload --port 8000

# 3. In another terminal, run tests (Terminal 2)
cd C:\\Users\\RishiGupta\\SmartScreen
python backend/tests/test_production_api.py

# OR manually test with curl:
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/
""")

# ═══════════════════════════════════════════════════════════════════════════
# QUICK TEST
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("🧪 QUICK VALIDATION TEST")
print("=" * 80)

try:
    print("\nTesting imports (this will verify everything is correct)...")
    from backend.config import settings
    print("  ✅ backend.config.settings imported")
    
    from backend.db.connection import engine
    print("  ✅ backend.db.connection.engine imported")
    
    from backend.services.parsing_service import parse_resume, parse_jd, match_resume_to_jd
    print("  ✅ backend.services.parsing_service imported")
    
    from backend.routes import auth_router, credit_router
    print("  ✅ backend.routes imported")
    
    print("\n✅ ALL IMPORTS SUCCESSFUL!")
    print("   Your application is ready to run:")
    print(f"   python -m uvicorn backend.main:app --reload --port 8000")
    
except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("\nThis means you're still in the wrong directory or dependencies are missing.")
    print("Make sure you're in: C:\\Users\\RishiGupta\\SmartScreen")

print("\n" + "=" * 80)
