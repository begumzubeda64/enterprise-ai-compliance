import uuid
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        db: AsyncSession,
        model: type[ModelType],
    ):
        self.db = db
        self.model = model

    async def create(
        self,
        entity: ModelType,
    ) -> ModelType:
        self.db.add(entity)

        await self.db.flush()
        await self.db.refresh(entity)

        return entity

    async def get_by_id(
        self,
        entity_id: uuid.UUID,
    ) -> ModelType | None:
        result = await self.db.execute(
            select(self.model).where(
                self.model.id == entity_id
            )
        )

        return result.scalar_one_or_none()