from app.repositories.compliance_framework_repository import (
    ComplianceFrameworkRepository,
)
from app.schemas.common.pagination import (
    PaginatedResponse,
    PaginationParams,
)
from app.schemas.compliance_framework import (
    ComplianceFrameworkResponse,
)
from app.exceptions.compliance_framework import (
    ComplianceFrameworkNotFoundException,
)
from uuid import UUID


class ComplianceFrameworkService:

    def __init__(
        self,
        repository: ComplianceFrameworkRepository,
    ):
        self.repository = repository

    async def list_frameworks(
        self,
        pagination: PaginationParams,
    ) -> PaginatedResponse[
        ComplianceFrameworkResponse
    ]:

        frameworks, total = (
            await self.repository.list(
                pagination,
            )
        )

        return PaginatedResponse[
            ComplianceFrameworkResponse
        ](
            items=[
                ComplianceFrameworkResponse.model_validate(
                    framework
                )
                for framework in frameworks
            ],
            total=total,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_framework(
        self,
        framework_id: UUID,
    ) -> ComplianceFrameworkResponse:

        framework = await self.repository.get_by_id(
            framework_id,
        )

        if framework is None:
            raise ComplianceFrameworkNotFoundException(
                framework_id
            )

        return ComplianceFrameworkResponse.model_validate(
            framework
        )