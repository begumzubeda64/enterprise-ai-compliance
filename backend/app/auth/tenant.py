from uuid import UUID

from app.exceptions.compliance_project import (
    OrganizationMembershipRequiredException,
)
from app.models.user import User


def get_user_organization_id(
    current_user: User,
) -> UUID:
    """
    Return the authenticated user's organization ID.

    Raises an application exception when the user does not
    belong to an organization.
    """

    if current_user.organization_id is None:
        raise OrganizationMembershipRequiredException()

    return current_user.organization_id