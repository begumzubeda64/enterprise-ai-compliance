from uuid import UUID

from fastapi import APIRouter, Depends

from app.dependencies.services import (
    get_compliance_framework_service,
)
from app.schemas.common.pagination import (
    PaginatedResponse,
    PaginationParams,
)
from app.schemas.compliance_framework import (
    ComplianceFrameworkResponse,
)
from app.services.compliance_framework_service import (
    ComplianceFrameworkService,
)

router = APIRouter(
    prefix="/frameworks",
    tags=["Compliance Frameworks"],
)


@router.get(
    "",
    response_model=PaginatedResponse[
        ComplianceFrameworkResponse
    ],
    summary="List Compliance Frameworks",
)
async def list_frameworks(
    pagination: PaginationParams = Depends(),
    service: ComplianceFrameworkService = Depends(
        get_compliance_framework_service,
    ),
):

    return await service.list_frameworks(
        pagination,
    )


@router.get(
    "/{framework_id}",
    response_model=ComplianceFrameworkResponse,
    summary="Get Compliance Framework",
)
async def get_framework(
    framework_id: UUID,
    service: ComplianceFrameworkService = Depends(
        get_compliance_framework_service,
    ),
):

    return await service.get_framework(
        framework_id,
    )