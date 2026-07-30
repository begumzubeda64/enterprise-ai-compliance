from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import configure_logging, logger

import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application lifecycle.

    This function is executed:
    - once during startup
    - once during shutdown
    """

    configure_logging()

    logger.info(
        "application_startup",
        app_name=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        process_id=os.getpid(),
    )

    try:
        yield

    finally:
        logger.info(
            "application_shutdown",
            app_name=settings.app_name,
        )