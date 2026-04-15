from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import backend module
root_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root_dir))

# Load .env from root
root_env = root_dir / ".env"
if root_env.exists():
    load_dotenv(dotenv_path=str(root_env))
else:
    load_dotenv()

from backend.db.connection import engine, Base


def main():
    """Create all database tables."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ ERROR: DATABASE_URL not set in .env file")
        print("Create .env file in SmartScreen root with:")
        print("  DATABASE_URL=postgresql://...")
        sys.exit(1)
    
    try:
        print("🔗 Connecting to database...")
        print(f"   DATABASE_URL: {db_url[:60]}...")
        Base.metadata.create_all(bind=engine)
        print("✅ DB tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
