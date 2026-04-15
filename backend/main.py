from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os
from backend.db.connection import engine, Base
from backend.config import settings
from backend.routes import auth_router, credit_router, billing_router, resume_router, jd_router, match_router
from backend.models import user, transaction, usage  # register all ORM models with Base

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api_title,
        description="Training & Placement SaaS Platform for Resume-JD Matching",
        version=settings.api_version,
        docs_url="/docs",
        redoc_url="/redoc" if not settings.is_production else None,
    )
    
    # Add CORS middleware with configured origins

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    # Include routers
    app.include_router(auth_router)
    app.include_router(credit_router)
    app.include_router(billing_router)
    app.include_router(resume_router)
    app.include_router(jd_router)
    app.include_router(match_router)
    
    logger.info(f"✅ SmartScreen API initialized ({settings.environment})")
    return app


app = create_app()


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    try:
        # Ensure DB tables exist on startup
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables verified")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        raise


@app.get("/")
def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "SmartScreen SaaS API",
        "version": settings.api_version,
        "environment": settings.environment
    }


@app.get("/health")
def health():
    """Health check for load balancers and monitoring."""
    try:
        # Test database connection
        from backend.db.connection import SessionLocal
        db = SessionLocal()
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "service": "SmartScreen API v" + settings.api_version
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }, 503


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
