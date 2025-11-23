from typing import Any, Optional
from urllib.parse import urlencode

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from . import app


class LoginException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = "Invalid login credentials",
        headrs: Optional[dict[str, str]] = None,
    ) -> None:
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headrs,
        )


@app.exception_handler(LoginException)
def auth_exception_handler(request: Request, exc: HTTPException) -> RedirectResponse:
    login_url = f"/login?{urlencode(
        {
            "redirect_url": request.url,
        }
    )}"
    return RedirectResponse(url=login_url, status_code=303)
