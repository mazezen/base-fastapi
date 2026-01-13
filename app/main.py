from loguru import logger
from fastapi import FastAPI
from app.common.config import settings
from app.common.logger import setup_logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from app.middlewares.logging_middleware import LoginMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.exceptions.exception import BaseError
from app.exceptions.exception_hanlder import http_exception_handler
from app.api import router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    setup_logging()
    logger.info("Running application startup tasks...")

    yield

    # Shutdown
    logger.info("Running application shutdown tasks...")

def run_application() -> FastAPI: 
    """Create FastAPI application."""
    logger.info("Starting application...")
    
    application = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan,
    )

    # Add Logging Middleware
    application.add_middleware(LoginMiddleware)

    # Set CORS Middleware
    if settings.ALLOW_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Add exception handler
    application.add_exception_handler(BaseError, http_exception_handler)

    # Add routes
    application.include_router(router, prefix=settings.API_V1_STR)

    logger.info("Application startup complete...")
    return application

app = run_application()