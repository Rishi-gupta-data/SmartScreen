from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
import os
import time
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
        redirect_slashes=False,  # ✅ Disable automatic trailing slash redirect
    )
    
    # ===== MIDDLEWARE: Request Logging =====
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all incoming requests with timing."""
        request_time = time.time()
        response = await call_next(request)
        process_time = time.time() - request_time
        
        # Log request details
        logger.info(
            f"{request.method} {request.url.path} | "
            f"Status: {response.status_code} | "
            f"Duration: {process_time:.3f}s"
        )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    # Add CORS middleware with configured origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    
    # ===== ROUTES: Include versioned routers =====
    # Prefix all routes with /api/v1 for future compatibility
    api_v1_prefix = "/api/v1"
    
    app.include_router(auth_router, prefix=api_v1_prefix)
    app.include_router(credit_router, prefix=api_v1_prefix)
    app.include_router(billing_router, prefix=api_v1_prefix)
    app.include_router(resume_router, prefix=api_v1_prefix)
    app.include_router(jd_router, prefix=api_v1_prefix)
    app.include_router(match_router, prefix=api_v1_prefix)
    
    logger.info(f"✅ SmartScreen API v{settings.api_version} initialized ({settings.environment})")
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
        "version": f"v{settings.api_version}",
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
            "service": f"SmartScreen API v{settings.api_version}"
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
