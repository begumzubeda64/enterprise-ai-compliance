from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"
    USER = "USER"


class RequirementSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ProjectStatus(str, Enum):
    DRAFT = "DRAFT"
    IN_REVIEW = "IN_REVIEW"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"