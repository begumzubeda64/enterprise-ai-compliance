from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings


def create_access_token(
    subject: str,
) -> str:
    """
    Create a signed JWT access token.
    """

    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "type": "access",
        "iat": now,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(
    token: str,
) -> dict:

    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )