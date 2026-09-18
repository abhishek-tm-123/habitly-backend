from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


# -------------------------
# Password hashing
# -------------------------

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError("Password cannot be longer than 72 bytes")

    return bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    password_bytes = password.encode("utf-8")
    hashed_password_bytes = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        password_bytes,
        hashed_password_bytes,
    )

#---------------------------
#   jwt
#--------------------------

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

def verify_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise JWTError

        return int(user_id)

    except (JWTError, ValueError):
        raise ValueError("Invalid or expired token")