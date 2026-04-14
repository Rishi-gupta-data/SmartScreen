from dotenv import load_dotenv
from backend.db.connection import engine, Base
import os
from pathlib import Path

# Explicitly load the repository root .env to avoid parsing malformed backend/.env
root_env = Path(__file__).resolve().parents[1] / ".env"
if root_env.exists():
    load_dotenv(dotenv_path=str(root_env))
else:
    load_dotenv()


def main():
    print("Creating DB tables using DATABASE_URL:", os.getenv("DATABASE_URL"))
    Base.metadata.create_all(bind=engine)
    print("DB tables created (or already exist).")


if __name__ == "__main__":
    main()
