from uuid import UUID

from app.exceptions.base import ResourceNotFoundException


class ComplianceFrameworkNotFoundException(
    ResourceNotFoundException,
):
    error_code = "COMPLIANCE_FRAMEWORK_NOT_FOUND"

    def __init__(
        self,
        framework_id: UUID,
    ):
        super().__init__(
            message=f"Compliance framework '{framework_id}' was not found."
        )