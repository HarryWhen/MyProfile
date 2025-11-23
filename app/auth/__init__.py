from fastapi import Depends
from fastapi.requests import Request

from app import app as app
from app import config as config
from app.userprofile import User, get_user

from .exceptions import LoginException
from .routing import router as router
from .token import Token, get_claims


def oauth2_scheme(request: Request) -> Token:
    if not (token := request.cookies.get("token")):
        raise LoginException()
    return Token.model_validate_json(token)


def get_current_user(access_token: Token = Depends(oauth2_scheme)) -> User:
    if not (claims := get_claims(access_token)) or not (user := get_user(claims.sub)):
        raise LoginException()
    return user
