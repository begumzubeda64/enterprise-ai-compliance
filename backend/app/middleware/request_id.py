from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
)


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        clear_contextvars()

        request_id = (
            request.headers.get("X-Request-ID")
            or str(uuid4())
        )

        request.state.request_id = request_id

        bind_contextvars(
            request_id=request_id,
        )

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        clear_contextvars()

        return response