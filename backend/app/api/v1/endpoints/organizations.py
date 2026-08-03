from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_organization_service
from app.schemas.organization import (
    OrganizationOnboardRequest,
    OrganizationOnboardResponse,
    OrganizationResponse,
)
from app.schemas.user import UserResponse
from app.services.organization_service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.post(
    "/onboard",
    response_model=OrganizationOnboardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Onboard Organization",
)
async def onboard_organization(
    payload: OrganizationOnboardRequest,
    service: OrganizationService = Depends(
        get_organization_service
    ),
) -> OrganizationOnboardResponse:

    organization, admin = await service.onboard_organization(
        payload
    )

    return OrganizationOnboardResponse(
        organization=OrganizationResponse.model_validate(
            organization
        ),
        admin=UserResponse.model_validate(admin),
    )