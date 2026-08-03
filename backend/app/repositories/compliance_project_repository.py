from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.compliance_project import ComplianceProject
from app.repositories.base_repository import BaseRepository
from app.schemas.common.pagination import PaginationParams


class ComplianceProjectRepository(
    BaseRepository[ComplianceProject]
):

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db=db,
            model=ComplianceProject,
        )

    async def get_by_id_and_organization(
        self,
        project_id: UUID,
        organization_id: UUID,
    ) -> ComplianceProject | None:
        result = await self.db.execute(
            select(ComplianceProject).where(
                ComplianceProject.id == project_id,
                ComplianceProject.organization_id
                == organization_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_by_organization(
        self,
        organization_id: UUID,
        pagination: PaginationParams,
    ) -> tuple[list[ComplianceProject], int]:
        total = await self.db.scalar(
            select(func.count())
            .select_from(ComplianceProject)
            .where(
                ComplianceProject.organization_id
                == organization_id
            )
        )

        result = await self.db.execute(
            select(ComplianceProject)
            .where(
                ComplianceProject.organization_id
                == organization_id
            )
            .order_by(
                ComplianceProject.created_at.desc()
            )
            .offset(pagination.offset)
            .limit(pagination.limit)
        )

        projects = list(
            result.scalars().all()
        )

        return projects, total or 0