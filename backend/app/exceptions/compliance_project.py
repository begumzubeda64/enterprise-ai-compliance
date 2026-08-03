from uuid import UUID

from app.exceptions.base import (
    BadRequestException,
    ResourceNotFoundException,
)


class ComplianceProjectNotFoundException(
    ResourceNotFoundException
):
    error_code = "COMPLIANCE_PROJECT_NOT_FOUND"

    def __init__(
        self,
        project_id: UUID,
    ):
        super().__init__(
            message=(
                f"Compliance project '{project_id}' "
                "was not found."
            )
        )


class OrganizationMembershipRequiredException(
    BadRequestException
):
    error_code = "ORGANIZATION_MEMBERSHIP_REQUIRED"

    def __init__(self):
        super().__init__(
            message=(
                "The authenticated user must belong to "
                "an organization."
            )
        )