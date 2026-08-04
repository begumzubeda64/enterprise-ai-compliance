from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.compliance_documents import (
    router as compliance_documents_router,
)
from app.api.v1.endpoints.compliance_frameworks import (
    router as compliance_frameworks_router,
)
from app.api.v1.endpoints.compliance_projects import (
    router as compliance_projects_router,
)
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.organizations import (
    router as organizations_router,
)
from app.api.v1.endpoints.users import router as users_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(organizations_router)
api_router.include_router(compliance_frameworks_router)
api_router.include_router(compliance_projects_router)
api_router.include_router(compliance_documents_router)