"""
🔍 SmartScreen Diagnostic & Debug Script
Checks all environment setup issues
"""

import os
import sys
from pathlib import Path

print("=" * 80)
print("SmartScreen Diagnostics & Debug Report")
print("=" * 80)

# ═══════════════════════════════════════════════════════════════════════════
# 1. CHECK WORKING DIRECTORY
# ═══════════════════════════════════════════════════════════════════════════
print("\n1️⃣  WORKING DIRECTORY")
print("─" * 80)

cwd = Path.cwd()
print(f"Current directory: {cwd}")
print(f"Directory name: {cwd.name}")

smartscreen_root = Path("C:\\Users\\RishiGupta\\SmartScreen")
print(f"Expected root: {smartscreen_root}")
print(f"Root exists: {smartscreen_root.exists()}")

if cwd.name == "backend":
    print("⚠️  ERROR: You're in the 'backend' directory!")
    print("✅ FIX: Change to SmartScreen root first:")
    print("   cd C:\\Users\\RishiGupta\\SmartScreen")
elif cwd == smartscreen_root:
    print("✅ Correct directory!")
else:
    print(f"⚠️  WARNING: Not in expected location")

# ═══════════════════════════════════════════════════════════════════════════
# 2. CHECK .ENV FILE
# ═══════════════════════════════════════════════════════════════════════════
print("\n2️⃣  ENVIRONMENT FILE (.env)")
print("─" * 80)

env_file = cwd / ".env"
env_example = cwd / ".env.example"

print(f".env exists: {env_file.exists()}")
print(f".env.example exists: {env_example.exists()}")

if not env_file.exists():
    print("⚠️  ERROR: .env file not found!")
    print("✅ FIX: Create it from template:")
    print("   copy .env.example .env")
    print("   Then edit .env and add DATABASE_URL and SECRET_KEY")
else:
    print("✅ .env file exists")
    try:
        with open(env_file) as f:
            content = f.read()
            lines = [l for l in content.split('\n') if l and not l.startswith('#')]
            print(f"   Entries found: {len(lines)}")
            for line in lines[:3]:
                key = line.split('=')[0]
                print(f"   - {key}")
    except Exception as e:
        print(f"   Error reading: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. CHECK PYTHON PATH
# ═══════════════════════════════════════════════════════════════════════════
print("\n3️⃣  PYTHON PATH")
print("─" * 80)

print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

print(f"\nPython path entries:")
for i, p in enumerate(sys.path[:5]):
    print(f"  {i}: {p}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. CHECK BACKEND FOLDER STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════
print("\n4️⃣  BACKEND FOLDER STRUCTURE")
print("─" * 80)

backend_dir = cwd / "backend"
print(f"backend/ exists: {backend_dir.exists()}")

if backend_dir.exists():
    files = list(backend_dir.glob("*.py"))
    print(f"Python files in backend/: {len(files)}")
    for f in sorted(files)[:5]:
        print(f"  ✅ {f.name}")

    # Check subfolders
    for subdir in ["db", "models", "routes", "services", "tests", "schemas"]:
        path = backend_dir / subdir
        print(f"  {subdir}/ exists: {path.exists()}")

# ═══════════════════════════════════════════════════════════════════════════
# 5. CHECK IMPORTS IN main.py
# ═══════════════════════════════════════════════════════════════════════════
print("\n5️⃣  IMPORTS IN main.py")
print("─" * 80)

main_py = backend_dir / "main.py"
if main_py.exists():
    with open(main_py) as f:
        lines = f.readlines()[:30]
        imports = [l.strip() for l in lines if 'import' in l or 'from' in l]
    
    print(f"Import statements found in main.py:")
    for imp in imports[:8]:
        print(f"  {imp}")
        # Check if module exists
        if "from backend" in imp:
            module_path = imp.split("from backend.")[1].split(" import")[0].replace(".", "\\")
            full_path = backend_dir / module_path
            exists = full_path.exists() or (full_path.parent / (full_path.name + ".py")).exists()
            status = "✅" if exists else "❌"
            print(f"    {status} backend.{module_path}")
else:
    print("❌ main.py not found")

# ═══════════════════════════════════════════════════════════════════════════
# 6. CHECK DEPENDENCIES
# ═══════════════════════════════════════════════════════════════════════════
print("\n6️⃣  INSTALLED DEPENDENCIES")
print("─" * 80)

required = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "python_jose", "argon2"]
missing = []

for package in required:
    try:
        __import__(package.replace("-", "_"))
        print(f"  ✅ {package}")
    except ImportError:
        print(f"  ❌ {package} (MISSING)")
        missing.append(package)

if missing:
    print(f"\n⚠️  Missing packages: {', '.join(missing)}")
    print("✅ FIX: Install with:")
    print("   pip install -r requirements-prod.txt")

# ═══════════════════════════════════════════════════════════════════════════
# 7. CHECK DATABASE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════
print("\n7️⃣  DATABASE CONFIGURATION")
print("─" * 80)

try:
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    db_url = os.getenv("DATABASE_URL")
    secret_key = os.getenv("SECRET_KEY")
    environment = os.getenv("ENVIRONMENT", "development")
    
    print(f"ENVIRONMENT: {environment}")
    print(f"SECRET_KEY set: {'✅' if secret_key else '❌'}")
    print(f"DATABASE_URL set: {'✅' if db_url else '❌'}")
    
    if db_url:
        # Mask password
        if "@" in db_url:
            parts = db_url.split("@")
            print(f"  User part: {parts[0][:30]}...")
            print(f"  Host: {parts[1][:50]}...")
        else:
            print(f"  URL: {db_url[:50]}...")
    else:
        print("  ❌ DATABASE_URL not configured")
        
except Exception as e:
    print(f"  Error loading config: {e}")

# ═══════════════════════════════════════════════════════════════════════════
# 8. SUMMARY & FIXES
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("📋 QUICK FIXES")
print("=" * 80)

issues = []

if cwd.name == "backend":
    issues.append(("Wrong directory", "cd C:\\Users\\RishiGupta\\SmartScreen"))

if not env_file.exists():
    issues.append(("Missing .env", "copy .env.example .env"))

if missing:
    issues.append(("Missing packages", "pip install -r requirements-prod.txt"))

if issues:
    print("\n⚠️  Issues found:\n")
    for i, (issue, fix) in enumerate(issues, 1):
        print(f"{i}. {issue}")
        print(f"   ▶️  {fix}\n")
else:
    print("\n✅ No major issues detected!")

# ═══════════════════════════════════════════════════════════════════════════
# 9. CORRECT COMMAND
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 80)
print("✅ CORRECT COMMANDS TO RUN")
print("=" * 80)

print("""
# Terminal 1: Start the API server
cd C:\\Users\\RishiGupta\\SmartScreen
python -m uvicorn backend.main:app --reload --port 8000

# Terminal 2: Run diagnostics again
cd C:\\Users\\RishiGupta\\SmartScreen
python diagnostics.py

# Terminal 3: Initialize database (if needed)
cd C:\\Users\\RishiGupta\\SmartScreen
python -c "from backend.create_tables import create_schema; create_schema()"
""")

print("=" * 80)
