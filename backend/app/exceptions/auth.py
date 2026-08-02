from app.exceptions.base import (
    ForbiddenException,
    UnauthorizedException,
)


class InvalidCredentialsException(UnauthorizedException):
    error_code = "INVALID_CREDENTIALS"

    def __init__(self):
        super().__init__(
            message="Invalid email or password."
        )


class InvalidTokenException(UnauthorizedException):
    error_code = "INVALID_TOKEN"

    def __init__(self):
        super().__init__(
            message="Invalid or expired authentication token."
        )


class InactiveUserException(ForbiddenException):
    error_code = "INACTIVE_USER"

    def __init__(self):
        super().__init__(
            message="User account is inactive."
        )


class InsufficientPermissionsException(ForbiddenException):
    error_code = "INSUFFICIENT_PERMISSIONS"

    def __init__(self):
        super().__init__(
            message="You do not have permission to perform this action."
        )