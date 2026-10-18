from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.routers.auth import router as auth_router
from backend.app.routers.ventures import router as ventures_router
from backend.app.routers.worker import router as worker_router
from backend.app.routers.investor import router as investor_router

app = FastAPI(
    title="VentureForge AI API",
    description="Autonomous venture formation and co-founder intelligence platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.ENV,
        "database": "connected"
    }

# Mount /api/v1 routes
app.include_router(auth_router, prefix="/api/v1")
app.include_router(ventures_router, prefix="/api/v1")
app.include_router(worker_router, prefix="/api/v1")
app.include_router(investor_router, prefix="/api/v1")
