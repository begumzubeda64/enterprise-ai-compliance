from app.exceptions.base import (
    ConflictException,
    ResourceNotFoundException,
)


class UserAlreadyExistsException(ConflictException):
    error_code = "USER_ALREADY_EXISTS"

    def __init__(self, email: str):
        super().__init__(
            message=f"User with email '{email}' already exists."
        )


class UserNotFoundException(ResourceNotFoundException):
    error_code = "USER_NOT_FOUND"

    def __init__(self):
        super().__init__(
            message="User not found."
        )