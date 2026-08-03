from app.exceptions.base import ConflictException


class OrganizationSlugAlreadyExistsException(ConflictException):
    error_code = "ORGANIZATION_SLUG_ALREADY_EXISTS"

    def __init__(self, slug: str):
        super().__init__(
            message=f"Organization with slug '{slug}' already exists."
        )