from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from app import config
from app.userprofile import User, get_user

from .security import authenticate_user
from .token import Token, create_token, get_subject

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


login_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid login credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token validation failed",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(access_token: str = Depends(oauth2_scheme)) -> User:
    try:
        current_username = get_subject(access_token)
    except InvalidTokenError:
        raise token_exception
    if not (user := get_user(current_username)):
        raise token_exception
    return user


@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    if not (user := authenticate_user(form_data.username, form_data.password)):
        raise login_exception
    return create_token(user.username)
