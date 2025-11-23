from datetime import datetime, timedelta, timezone

import jwt
from pydantic import BaseModel

from utils import soft_call

from . import config


class JWTClaims(BaseModel):
    sub: str
    exp: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


@soft_call()
def get_claims(token: Token) -> JWTClaims:
    raw_claims = jwt.decode(
        token.access_token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
    )
    return JWTClaims.model_validate(raw_claims)


def create_access_token(claims: BaseModel) -> str:
    return jwt.encode(
        claims.model_dump(),
        config.SECRET_KEY,
        algorithm=config.ALGORITHM,
    )


def create_claims(subject: str, expires_delta: timedelta | None = None) -> JWTClaims:
    expire = datetime.now(timezone.utc) + (
        expires_delta or config.ACCESS_TOKEN_EXPIRES_DELTA
    )
    return JWTClaims(
        sub=subject,
        exp=expire,
    )


def create_token(subject: str, expires_delta: timedelta | None = None) -> Token:
    claims = create_claims(
        subject,
        expires_delta,
    )
    return Token(
        access_token=create_access_token(claims),
        token_type="bearer",
    )
