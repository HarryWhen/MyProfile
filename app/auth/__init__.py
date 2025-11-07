from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from app import app, config
from app.userprofile import User, get_user

from .security import authenticate_user
from .token import Token, create_token, get_subject

router = APIRouter()


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


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> RedirectResponse:
    if not (user := authenticate_user(form_data.username, form_data.password)):
        raise LoginException()
    response = RedirectResponse("/myprofile", 303)
    response.set_cookie(
        "access_token",
        create_token(user.username).access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response


@router.get("/login")
def read_login(request: Request) -> HTMLResponse:
    from fastapi.templating import Jinja2Templates

    templates = Jinja2Templates(directory=config.TEMPLATES_DIRECTORY)
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )
