from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from jwt.exceptions import InvalidTokenError

from app import app, config
from app.userprofile import User, get_user

from .token import Token, create_token, get_subject


class LoginException(HTTPException):
    def __init__(self, *args, **kwargs) -> None:
        kwargs = {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "detail": "Invalid login credentials",
            **kwargs,
        }
        super().__init__(
            *args,
            **kwargs,
        )


@app.exception_handler(LoginException)
def auth_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/login", status_code=303)


def oauth2_scheme(request: Request) -> Optional[str]:
    return request.cookies.get("access_token")


def get_current_user(access_token: str = Depends(oauth2_scheme)) -> User:
    try:
        current_username = get_subject(access_token)
    except InvalidTokenError:
        raise LoginException()
    if not (user := get_user(current_username)):
        raise LoginException()
    return user
