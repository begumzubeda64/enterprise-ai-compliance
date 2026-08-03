from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.compliance_framework import (
    ComplianceFrameworkNotFoundException,
)
from app.exceptions.compliance_project import (
    ComplianceProjectNotFoundException,
    OrganizationMembershipRequiredException,
)
from app.models.compliance_project import ComplianceProject
from app.models.enums import ProjectStatus
from app.models.user import User
from app.repositories.compliance_framework_repository import (
    ComplianceFrameworkRepository,
)
from app.repositories.compliance_project_repository import (
    ComplianceProjectRepository,
)
from app.schemas.common.pagination import (
    PaginatedResponse,
    PaginationParams,
)
from app.schemas.compliance_project import (
    ComplianceProjectCreate,
    ComplianceProjectResponse,
)


class ComplianceProjectService:

    def __init__(
        self,
        project_repository: ComplianceProjectRepository,
        framework_repository: ComplianceFrameworkRepository,
        db: AsyncSession,
    ):
        self.project_repository = project_repository
        self.framework_repository = framework_repository
        self.db = db

    async def create_project(
        self,
        project_data: ComplianceProjectCreate,
        current_user: User,
    ) -> ComplianceProjectResponse:
        organization_id = self._get_organization_id(
            current_user
        )

        framework = (
            await self.framework_repository.get_by_id(
                project_data.framework_id
            )
        )

        if framework is None:
            raise ComplianceFrameworkNotFoundException(
                project_data.framework_id
            )

        project = ComplianceProject(
            organization_id=organization_id,
            framework_id=framework.id,
            created_by=current_user.id,
            name=project_data.name,
            description=project_data.description,
            status=ProjectStatus.DRAFT,
        )

        try:
            created_project = (
                await self.project_repository.create(
                    project
                )
            )

            await self.db.commit()
            await self.db.refresh(created_project)

        except Exception:
            await self.db.rollback()
            raise

        return ComplianceProjectResponse.model_validate(
            created_project
        )

    async def list_projects(
        self,
        pagination: PaginationParams,
        current_user: User,
    ) -> PaginatedResponse[
        ComplianceProjectResponse
    ]:
        organization_id = self._get_organization_id(
            current_user
        )

        projects, total = (
            await self.project_repository.list_by_organization(
                organization_id=organization_id,
                pagination=pagination,
            )
        )

        return PaginatedResponse[
            ComplianceProjectResponse
        ](
            items=[
                ComplianceProjectResponse.model_validate(
                    project
                )
                for project in projects
            ],
            total=total,
            offset=pagination.offset,
            limit=pagination.limit,
        )

    async def get_project(
        self,
        project_id: UUID,
        current_user: User,
    ) -> ComplianceProjectResponse:
        organization_id = self._get_organization_id(
            current_user
        )

        project = (
            await self.project_repository
            .get_by_id_and_organization(
                project_id=project_id,
                organization_id=organization_id,
            )
        )

        if project is None:
            raise ComplianceProjectNotFoundException(
                project_id
            )

        return ComplianceProjectResponse.model_validate(
            project
        )

    @staticmethod
    def _get_organization_id(
        current_user: User,
    ) -> UUID:
        if current_user.organization_id is None:
            raise OrganizationMembershipRequiredException()

        return current_user.organization_id