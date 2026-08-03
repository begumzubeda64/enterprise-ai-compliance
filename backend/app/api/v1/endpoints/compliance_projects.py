from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.auth.authorization import require_roles
from app.auth.dependencies import get_current_user
from app.dependencies.services import (
    get_compliance_project_service,
)
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.common.pagination import (
    PaginatedResponse,
    PaginationParams,
)
from app.schemas.compliance_project import (
    ComplianceProjectCreate,
    ComplianceProjectResponse,
)
from app.services.compliance_project_service import (
    ComplianceProjectService,
)

router = APIRouter(
    prefix="/projects",
    tags=["Compliance Projects"],
)


@router.post(
    "",
    response_model=ComplianceProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Compliance Project",
)
async def create_project(
    payload: ComplianceProjectCreate,
    current_user: User = Depends(
        require_roles(
            UserRole.ADMIN,
            UserRole.REVIEWER,
            UserRole.USER,
        )
    ),
    service: ComplianceProjectService = Depends(
        get_compliance_project_service
    ),
) -> ComplianceProjectResponse:
    return await service.create_project(
        project_data=payload,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=PaginatedResponse[
        ComplianceProjectResponse
    ],
    summary="List Compliance Projects",
)
async def list_projects(
    pagination: PaginationParams = Depends(),
    current_user: User = Depends(get_current_user),
    service: ComplianceProjectService = Depends(
        get_compliance_project_service
    ),
) -> PaginatedResponse[
    ComplianceProjectResponse
]:
    return await service.list_projects(
        pagination=pagination,
        current_user=current_user,
    )


@router.get(
    "/{project_id}",
    response_model=ComplianceProjectResponse,
    summary="Get Compliance Project",
)
async def get_project(
    project_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ComplianceProjectService = Depends(
        get_compliance_project_service
    ),
) -> ComplianceProjectResponse:
    return await service.get_project(
        project_id=project_id,
        current_user=current_user,
    )