from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.exceptions.user import UserAlreadyExistsException


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate) -> User:

        existing_user = await self.repository.get_by_email(user_data.email)

        if existing_user:
            raise UserAlreadyExistsException(user_data.email)

        user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=user_data.password,   # Temporary
        )

        return await self.repository.create(user)