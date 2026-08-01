from app.core.exceptions import ConflictException


class UserAlreadyExistsException(ConflictException):
    error_code = "USER_ALREADY_EXISTS"

    def __init__(self, email: str):
        super().__init__(
            message=f"User with email '{email}' already exists."
        )