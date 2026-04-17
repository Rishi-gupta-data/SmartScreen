#!/usr/bin/env python3
"""SmartScreen Development Server Startup"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_env():
    """Check if environment is properly configured"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("   Please create .env or copy from config/.env.example")
        return False
    
    print("✓ .env file found")
    return True

def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import uvicorn
        print("✓ Backend dependencies OK")
    except ImportError:
        print("❌ Backend dependencies missing!")
        print("   Run: pip install -r requirements.txt")
        return False
    
    # Check Node.js
    result = subprocess.run(["node", "--version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ Node.js not found!")
        print("   Please install Node.js 16+")
        return False
    
    print("✓ Node.js found:", result.stdout.strip())
    return True

def start_backend():
    """Start the backend server"""
    print("\n" + "="*60)
    print("STARTING BACKEND SERVER")
    print("="*60)
    
    cmd = [
        sys.executable, "-m", "uvicorn",
        "backend.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]
    
    print(f"\nCommand: {' '.join(cmd)}")
    print("\nBackend will be available at:")
    print("  - API: http://localhost:8000")
    print("  - Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop\n")
    
    subprocess.run(cmd)

def main():
    """Main startup function"""
    print("\n" + "="*60)
    print("SmartScreen Development Environment")
    print("="*60)
    
    # Check prerequisites
    print("\n[1/2] Checking environment...")
    if not check_env():
        sys.exit(1)
    
    print("\n[2/2] Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("ALL CHECKS PASSED!")
    print("="*60)
    
    print("\nNOTE: This script starts only the backend.")
    print("For frontend, run in a separate terminal:")
    print("  cd frontend && npm start")
    
    # Start backend
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n\nShutting down backend...")
        print("Goodbye!")

if __name__ == "__main__":
    main()
