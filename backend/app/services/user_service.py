from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.jwt import create_access_token
from app.auth.password import (
    hash_password,
    verify_password,
)
from app.exceptions.auth import InvalidCredentialsException
from app.exceptions.user import UserAlreadyExistsException
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate


class UserService:

    def __init__(
        self,
        repository: UserRepository,
        db: AsyncSession,
    ):
        self.repository = repository
        self.db = db

    async def create_user(
        self,
        user_data: UserCreate,
    ) -> User:
        existing_user = await self.repository.get_by_email(
            user_data.email
        )

        if existing_user:
            raise UserAlreadyExistsException(
                user_data.email
            )

        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(
                user_data.password
            ),
        )

        try:
            created_user = await self.repository.create(user)
            await self.db.commit()
            await self.db.refresh(created_user)

            return created_user

        except Exception:
            await self.db.rollback()
            raise

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> str:
        user = await self.repository.get_by_email(email)

        if (
            user is None
            or not verify_password(
                password,
                user.hashed_password,
            )
        ):
            raise InvalidCredentialsException()

        return create_access_token(
            subject=str(user.id),
        )