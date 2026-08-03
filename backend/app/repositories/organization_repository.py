from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.organization import Organization
from app.repositories.base_repository import BaseRepository


class OrganizationRepository(
    BaseRepository[Organization],
):

    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            db=db,
            model=Organization,
        )

    async def get_by_slug(
        self,
        slug: str,
    ) -> Organization | None:
        result = await self.db.execute(
            select(Organization).where(
                Organization.slug == slug
            )
        )

        return result.scalar_one_or_none()