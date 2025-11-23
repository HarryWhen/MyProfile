from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates

from utils import create_url

from . import config
from .exceptions import LoginException
from .password import authenticate_user
from .token import create_token

router = APIRouter()


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    redirect_url: Optional[str] = None,
) -> RedirectResponse:
    if not (user := authenticate_user(form_data.username, form_data.password)):
        raise LoginException()
    response = RedirectResponse(redirect_url or "", 303)
    response.set_cookie(
        "token",
        create_token(user.username).model_dump_json(),
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response


@router.get("/login")
def read_login(request: Request, redirect_url: Optional[str] = None) -> HTMLResponse:

    templates = Jinja2Templates(directory=config.TEMPLATES_DIRECTORY)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "token_url": create_url(
                "/token",
                {"redirect_url": redirect_url},
            )
        },
    )
