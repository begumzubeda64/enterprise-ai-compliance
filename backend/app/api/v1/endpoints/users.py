from fastapi import APIRouter, Depends, status

from app.dependencies.services import get_user_service

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
    """
    Create a new user.
    """

    return await service.create_user(payload)