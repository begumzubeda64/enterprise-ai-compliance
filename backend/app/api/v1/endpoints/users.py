from fastapi import APIRouter, Depends, status

from app.auth.authorization import require_roles
from app.auth.dependencies import get_current_user
from app.dependencies.services import get_user_service
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
)
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:

    return await service.create_user(payload)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Current User",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:

    return UserResponse.model_validate(current_user)


@router.get(
    "/admin",
    summary="Admin Only Endpoint",
)
async def admin_only(
    current_user: User = Depends(
        require_roles(UserRole.ADMIN)
    ),
):

    return {
        "message": "Welcome Admin",
        "user": current_user.email,
        "role": current_user.role,
    }