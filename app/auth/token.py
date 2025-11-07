from datetime import datetime, timedelta, timezone

import jwt
from pydantic import BaseModel

from . import config


class Token(BaseModel):
    access_token: str
    token_type: str


def get_subject(access_token: str) -> str:
    return jwt.decode(
        access_token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
    ).get("sub")


def create_token(subject: str, expires_delta: timedelta | None = None) -> Token:
    expire = datetime.now(timezone.utc) + (
        expires_delta or config.ACCESS_TOKEN_EXPIRES_DELTA
    )
    access_token = jwt.encode(
        {
            "sub": subject,
            "exp": expire,
        },
        config.SECRET_KEY,
        algorithm=config.ALGORITHM,
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
    )
