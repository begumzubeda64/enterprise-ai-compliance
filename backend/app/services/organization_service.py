from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import hash_password
from app.exceptions.organization import (
    OrganizationSlugAlreadyExistsException,
)
from app.exceptions.user import UserAlreadyExistsException
from app.models.enums import UserRole
from app.models.organization import Organization
from app.models.user import User
from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.user_repository import UserRepository
from app.schemas.organization import OrganizationOnboardRequest


class OrganizationService:

    def __init__(
        self,
        organization_repository: OrganizationRepository,
        user_repository: UserRepository,
        db: AsyncSession,
    ):
        self.organization_repository = organization_repository
        self.user_repository = user_repository
        self.db = db

    async def onboard_organization(
        self,
        onboarding_data: OrganizationOnboardRequest,
    ) -> tuple[Organization, User]:

        existing_organization = (
            await self.organization_repository.get_by_slug(
                onboarding_data.organization_slug
            )
        )

        if existing_organization:
            raise OrganizationSlugAlreadyExistsException(
                onboarding_data.organization_slug
            )

        existing_user = await self.user_repository.get_by_email(
            onboarding_data.admin_email
        )

        if existing_user:
            raise UserAlreadyExistsException(
                onboarding_data.admin_email
            )

        organization = Organization(
            name=onboarding_data.organization_name,
            slug=onboarding_data.organization_slug,
            description=onboarding_data.organization_description,
        )

        try:
            created_organization = (
                await self.organization_repository.create(
                    organization
                )
            )

            admin_user = User(
                organization_id=created_organization.id,
                email=onboarding_data.admin_email,
                full_name=onboarding_data.admin_full_name,
                hashed_password=hash_password(
                    onboarding_data.admin_password
                ),
                role=UserRole.ADMIN,
            )

            created_admin = await self.user_repository.create(
                admin_user
            )

            await self.db.commit()

            await self.db.refresh(created_organization)
            await self.db.refresh(created_admin)

            return created_organization, created_admin

        except Exception:
            await self.db.rollback()
            raise