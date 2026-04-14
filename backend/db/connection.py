import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configure database via the DATABASE_URL env var.
# For local development the default is SQLite. For production use a Postgres URL
# (e.g. Neon):
# DATABASE_URL=postgresql://<user>:<password>@<host>:5432/<db>?sslmode=require
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./smartscreen.db")

# SQLAlchemy engine. When using SQLite we need the check_same_thread connect arg.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
