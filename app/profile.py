from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from . import config
from .auth import get_current_user
from .userprofile import User, UserProfile, get_user_profile

router = APIRouter(prefix="/myprofile", default_response_class=HTMLResponse)

templates = Jinja2Templates(directory=config.TEMPLATES_DIRECTORY)


def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserProfile:
    return get_user_profile(current_user)


@router.get("/")
def read_my_profile(
    request: Request,
    current_user_profile: UserProfile = Depends(get_current_user_profile),
) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="myprofile.html",
        context=current_user_profile.dict(),
    )
