import asyncio
import sys

from app.core.logging import configure_logging, logger
from app.db.seed.compliance_frameworks import (
    seed_compliance_frameworks,
)
from app.db.session import AsyncSessionLocal


async def run_seeds() -> None:
    configure_logging()

    logger.info("database_seed_started")

    async with AsyncSessionLocal() as db:
        try:
            await seed_compliance_frameworks(db)

        except Exception:
            await db.rollback()
            logger.exception("database_seed_failed")
            raise

    logger.info("database_seed_completed")


if __name__ == "__main__":
    # Required only for Windows when using psycopg async.
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(
            asyncio.WindowsSelectorEventLoopPolicy()
        )

    asyncio.run(run_seeds())