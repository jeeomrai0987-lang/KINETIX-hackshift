import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from backend.app.config import settings
from backend.app.routers import auth, ventures, worker, investor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ventureforge")

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

# Standardized Error Responses (Section 8)
# errors are {"error": {"code": "string", "message": "string"}}

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": "http_error", "message": str(exc.detail)}}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    msg = "; ".join([f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in errors])
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": {"code": "validation_error", "message": msg}}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled server error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "internal_error", "message": "An unexpected server error occurred."}}
    )

# Health Check (Section 8)
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ventureforge-backend",
        "env": settings.ENV,
        "databaseConnected": True
    }

# Mount API routers at /api/v1
api_v1 = FastAPI(title="VentureForge AI v1")
app.mount("/api/v1", api_v1)

api_v1.include_router(auth.router)
api_v1.include_router(ventures.router)
api_v1.include_router(worker.router)
api_v1.include_router(investor.router)

# Also include routes on root app for /api/v1 directly if preferred
app.include_router(auth.router, prefix="/api/v1")
app.include_router(ventures.router, prefix="/api/v1")
app.include_router(worker.router, prefix="/api/v1")
app.include_router(investor.router, prefix="/api/v1")
