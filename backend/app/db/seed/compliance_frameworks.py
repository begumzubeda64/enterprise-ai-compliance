from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.compliance_framework import ComplianceFramework


FRAMEWORKS = [
    {
        "name": "EU AI Act",
        "version": "2024",
        "description": (
            "European Union regulation governing the development, "
            "deployment, and use of artificial intelligence systems."
        ),
    },
    {
        "name": "ISO/IEC 42001",
        "version": "2023",
        "description": (
            "International standard for establishing, implementing, "
            "maintaining, and improving an AI management system."
        ),
    },
    {
        "name": "NIST AI RMF",
        "version": "1.0",
        "description": (
            "NIST Artificial Intelligence Risk Management Framework "
            "for managing risks associated with AI systems."
        ),
    },
    {
        "name": "SOC 2",
        "version": "2022",
        "description": (
            "Compliance framework based on trust services criteria "
            "for security, availability, processing integrity, "
            "confidentiality, and privacy."
        ),
    },
]


async def seed_compliance_frameworks(
    db: AsyncSession,
) -> None:
    for framework_data in FRAMEWORKS:
        result = await db.execute(
            select(ComplianceFramework).where(
                ComplianceFramework.name
                == framework_data["name"],
                ComplianceFramework.version
                == framework_data["version"],
            )
        )

        existing_framework = result.scalar_one_or_none()

        if existing_framework is not None:
            continue

        db.add(
            ComplianceFramework(
                name=framework_data["name"],
                version=framework_data["version"],
                description=framework_data["description"],
                is_active=True,
            )
        )

    await db.commit()