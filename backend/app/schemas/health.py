from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    application: str
    version: str
    environment: str


class ReadinessResponse(BaseModel):
    status: str