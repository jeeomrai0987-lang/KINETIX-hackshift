from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from backend.app.core.config import settings
from backend.app.core.errors import (
    AppError,
    http_exception_handler,
    app_error_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from backend.app.routers import auth, ventures, worker, investor

def create_app() -> FastAPI:
    app = FastAPI(
        title="VentureForge AI API",
        version="1.0.0",
        description="Autonomous venture formation and co-founder intelligence platform backend API.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # CORS
    origins = settings.cors_origins_list
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins if origins != ["*"] else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception Handlers
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # Health Check
    @app.get("/health")
    def health_check():
        return {
            "status": "healthy",
            "service": "ventureforge-backend",
            "env": settings.ENV,
            "databaseConnected": True
        }

    # Mount routers under /api/v1
    app.include_router(auth.router, prefix="/api/v1")
    app.include_router(ventures.router, prefix="/api/v1")
    app.include_router(worker.router, prefix="/api/v1")
    app.include_router(investor.router, prefix="/api/v1")

    return app

app = create_app()
