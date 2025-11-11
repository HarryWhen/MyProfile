from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from . import LoginException, config
from .password import authenticate_user
from .token import create_token

router = APIRouter()


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
