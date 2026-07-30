from fastapi import APIRouter

from app.core.config import settings
from app.core.logging import configure_logging, logger
from app.schemas.health import (
    HealthResponse,
    ReadinessResponse,
)

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
)
async def health_check() -> HealthResponse:

    # logger.info("health_check_called")

    return HealthResponse(
        status="healthy",
        application=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness Check",
)
async def readiness_check() -> ReadinessResponse:

    return ReadinessResponse(
        status="ready",
    )