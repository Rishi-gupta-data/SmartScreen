#!/usr/bin/env python3
"""SmartScreen Directory Organization Script"""

import os
import shutil
from pathlib import Path

root = Path(".")

# Create directories
dirs = ["docs", "scripts", "tests", "config"]
for d in dirs:
    Path(d).mkdir(exist_ok=True)
    print(f"✓ Created {d}/")

# Documentation files
doc_files = [
    "README.md", "README_NEW.md", "QUICK_START.md", "QUICK_REFERENCE.md",
    "ADMIN_PANEL_GUIDE.md", "ADMIN_SETUP_QUICK_START.md",
    "API_DOCUMENTATION.md", "API_ENDPOINTS_VERIFICATION.md", "API_MATCHING_COMPLETE.md",
    "API_SYNC_COMPLETION_REPORT.md", "BACKEND_FRONTEND_MATCHING_REPORT.md", "BACKEND_SETUP.md",
    "COMPLETION_CHECKLIST.md", "DEPLOYMENT_GUIDE.md",
    "FRONTEND_API_FIXES_DETAILED.md", "FRONTEND_COMPLETE.md", "FRONTEND_CRITICAL_FIXES.md",
    "IMPLEMENTATION_SUMMARY.md", "PRODUCTION_BACKEND_IMPROVEMENTS.md", "PRODUCTION_STATUS.md",
    "SRS.md", "plan.md", "synthetic.md"
]

print("\nMoving documentation files...")
for f in doc_files:
    src = root / f
    if src.exists():
        shutil.move(str(src), f"docs/{f}")
        print(f"  docs/{f}")

# Script files
script_files = [
    "1.py", "check_admin.py", "check_db_urls.py", "create_admin_seed.py",
    "diagnose_backend.py", "diagnostics.py", "fix_startup.py", 
    "test_admin_endpoints.py", "test_login.py", "setup.bat", "setup.sh"
]

print("\nMoving script files...")
for f in script_files:
    src = root / f
    if src.exists():
        shutil.move(str(src), f"scripts/{f}")
        print(f"  scripts/{f}")

# Test files
test_files = ["test_output.txt", "test_results.txt"]

print("\nMoving test files...")
for f in test_files:
    src = root / f
    if src.exists():
        shutil.move(str(src), f"tests/{f}")
        print(f"  tests/{f}")

# Config files
config_files = ["Procfile", "skills.json"]

print("\nMoving config files...")
for f in config_files:
    src = root / f
    if src.exists():
        shutil.move(str(src), f"config/{f}")
        print(f"  config/{f}")

# Cleanup
if (root / "__pycache__").exists():
    shutil.rmtree(root / "__pycache__")
    print("\n✓ Removed __pycache__")

if (root / "smartscreen.db").exists():
    os.remove(root / "smartscreen.db")
    print("✓ Removed smartscreen.db (test database)")

print("\n" + "="*60)
print("DIRECTORY ORGANIZATION COMPLETE!")
print("="*60)
print("\nNew Structure:")
print("  SmartScreen/")
print("    ├── backend/           FastAPI application")
print("    ├── frontend/          React application")
print("    ├── docs/              Documentation files")
print("    ├── scripts/           Utility scripts")
print("    ├── tests/             Test files")
print("    ├── config/            Configuration files")
print("    ├── venv/              Python virtual environment")
print("    ├── .env               Environment variables")
print("    └── requirements.txt")
