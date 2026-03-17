"""
AI Data Analysis Agent - FastAPI application entry point.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: ensure upload dir exists. Shutdown: optional cleanup."""
    from app.utils.file_utils import ensure_upload_dir
    ensure_upload_dir()
    yield
    # Optional: clear in-memory dataset on shutdown
    # from app.services.dataset_service import dataset_service
    # dataset_service.clear()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Upload CSV/Excel datasets and get automatic EDA, correlation, anomaly detection, and LLM-generated insights.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    """Health and info."""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "upload": "POST /api/upload_dataset",
        "endpoints": [
            "GET /api/dataset_summary",
            "GET /api/correlation_analysis",
            "GET /api/anomaly_detection",
            "GET /api/ai_insights",
        ],
    }


@app.get("/health")
def health():
    """Health check for Docker/load balancers."""
    return {"status": "ok"}
