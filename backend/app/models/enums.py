from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"
    USER = "USER"