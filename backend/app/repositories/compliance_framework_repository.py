from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.compliance_framework import (
    ComplianceFramework,
)
from app.repositories.base_repository import BaseRepository
from app.schemas.common.pagination import PaginationParams


class ComplianceFrameworkRepository(
    BaseRepository[ComplianceFramework],
):

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db=db,
            model=ComplianceFramework,
        )

    async def list(
        self,
        pagination: PaginationParams,
    ) -> tuple[list[ComplianceFramework], int]:
        total = await self.db.scalar(
            select(func.count()).select_from(
                ComplianceFramework
            )
        )

        result = await self.db.execute(
            select(ComplianceFramework)
            .order_by(
                ComplianceFramework.name,
                ComplianceFramework.version,
            )
            .offset(pagination.offset)
            .limit(pagination.limit)
        )

        frameworks = list(
            result.scalars().all()
        )

        return frameworks, total or 0