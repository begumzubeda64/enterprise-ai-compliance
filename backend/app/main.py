from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.lifespan import lifespan

from app.middleware.request_id import RequestIDMiddleware
from app.middleware.logging import LoggingMiddleware

from app.core.handlers import register_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        contact={
            "name": settings.author_name,
            "url": settings.author_url,
        },
        license_info={
            "name": settings.license_name,
        },
    )

    register_exception_handlers(app)

    app.add_middleware(LoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    app.include_router(
        api_router,
        prefix=settings.api_v1_prefix,
    )

    return app


app = create_app()