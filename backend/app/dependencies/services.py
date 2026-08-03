from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.compliance_framework_repository import (
    ComplianceFrameworkRepository,
)
from app.repositories.compliance_project_repository import (
    ComplianceProjectRepository,
)
from app.repositories.organization_repository import (
    OrganizationRepository,
)
from app.repositories.user_repository import UserRepository
from app.services.compliance_framework_service import (
    ComplianceFrameworkService,
)
from app.services.compliance_project_service import (
    ComplianceProjectService,
)
from app.services.organization_service import OrganizationService
from app.services.user_service import UserService


def get_user_service(
    db: AsyncSession = Depends(get_db),
) -> UserService:
    repository = UserRepository(db)

    return UserService(
        repository=repository,
        db=db,
    )


def get_organization_service(
    db: AsyncSession = Depends(get_db),
) -> OrganizationService:
    return OrganizationService(
        organization_repository=OrganizationRepository(db),
        user_repository=UserRepository(db),
        db=db,
    )


def get_compliance_framework_service(
    db: AsyncSession = Depends(get_db),
) -> ComplianceFrameworkService:
    return ComplianceFrameworkService(
        repository=ComplianceFrameworkRepository(db),
    )


def get_compliance_project_service(
    db: AsyncSession = Depends(get_db),
) -> ComplianceProjectService:
    return ComplianceProjectService(
        project_repository=ComplianceProjectRepository(db),
        framework_repository=ComplianceFrameworkRepository(db),
        db=db,
    )