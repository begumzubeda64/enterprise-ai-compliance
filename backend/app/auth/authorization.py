from collections.abc import Callable
from typing import Any

from fastapi import Depends

from app.auth.dependencies import get_current_user
from app.exceptions.auth import InsufficientPermissionsException
from app.models.enums import UserRole
from app.models.user import User


def require_roles(
    *allowed_roles: UserRole,
) -> Callable[..., Any]:
    """
    Require the authenticated user to have one of the allowed roles.
    """

    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise InsufficientPermissionsException()

        return current_user

    return role_checker