from fastapi import FastAPI
from backend.db.connection import engine, Base
from backend.routes import auth_router, credit_router, resume_router, jd_router, match_router


def create_app() -> FastAPI:
    app = FastAPI(title="SmartScreen API")
    app.include_router(auth_router)
    app.include_router(credit_router)
    app.include_router(resume_router)
    app.include_router(jd_router)
    app.include_router(match_router)
    return app


app = create_app()
@app.on_event("startup")
def on_startup():
    # Ensure DB tables exist on startup (works when running under uvicorn)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
