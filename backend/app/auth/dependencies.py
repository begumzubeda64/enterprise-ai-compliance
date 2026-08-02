import uuid

from fastapi import Depends
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import decode_access_token
from app.auth.security import oauth2_scheme
from app.db.dependencies import get_db
from app.exceptions.auth import (
    InactiveUserException,
    InvalidTokenException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    try:
        payload = decode_access_token(token)

        subject = payload.get("sub")
        token_type = payload.get("type")

        if subject is None or token_type != "access":
            raise InvalidTokenException()

        user_id = uuid.UUID(subject)

    except (JWTError, ValueError, TypeError) as exc:
        raise InvalidTokenException() from exc

    repository = UserRepository(db)
    user = await repository.get_by_id(user_id)

    if user is None:
        raise InvalidTokenException()

    if not user.is_active:
        raise InactiveUserException()

    return user