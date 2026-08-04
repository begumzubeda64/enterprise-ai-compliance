from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.compliance_document import ComplianceDocument
from app.repositories.base_repository import BaseRepository
from app.schemas.common.pagination import PaginationParams


class ComplianceDocumentRepository(
    BaseRepository[ComplianceDocument]
):
    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db=db,
            model=ComplianceDocument,
        )

    async def list_by_project(
        self,
        project_id: UUID,
        pagination: PaginationParams,
    ) -> tuple[list[ComplianceDocument], int]:
        total = await self.db.scalar(
            select(func.count())
            .select_from(ComplianceDocument)
            .where(
                ComplianceDocument.project_id == project_id
            )
        )

        result = await self.db.execute(
            select(ComplianceDocument)
            .where(
                ComplianceDocument.project_id == project_id
            )
            .order_by(
                ComplianceDocument.created_at.desc()
            )
            .offset(pagination.offset)
            .limit(pagination.limit)
        )

        documents = list(
            result.scalars().all()
        )

        return documents, total or 0

    async def get_by_id_and_project(
        self,
        document_id: UUID,
        project_id: UUID,
    ) -> ComplianceDocument | None:
        result = await self.db.execute(
            select(ComplianceDocument).where(
                ComplianceDocument.id == document_id,
                ComplianceDocument.project_id == project_id,
            )
        )

        return result.scalar_one_or_none()