"""
Main FastAPI application.
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.shared.config import get_settings
from app.shared.logging_config import setup_logging, get_logger
from app.interfaces.api.v1 import api_router


# 设置日志
setup_logging()
logger = get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    logger.info("应用启动开始")

    # Startup tasks will be added here
    logger.info("应用启动完成")

    yield

    # Shutdown tasks (if needed)
    logger.info("应用关闭")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered flashcard application API",
    openapi_url="/api/v1/openapi.json" if settings.DEBUG else None,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "app": settings.APP_NAME
    }


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Documentation not available in production"
    }