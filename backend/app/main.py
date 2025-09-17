from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import Base, engine
from .api.routes.patients import router as patients_router
from .api.routes.upload import router as upload_router
from .api.routes.predict import router as predict_router
from .api.routes.reports import router as reports_router

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    Base.metadata.create_all(bind=engine)
    app.include_router(patients_router, prefix="/patients", tags=["patients"])
    app.include_router(upload_router, prefix="/upload", tags=["upload"])
    app.include_router(predict_router, tags=["predict"])
    app.include_router(reports_router, tags=["reports"])
    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}
    return app

app = create_app()
