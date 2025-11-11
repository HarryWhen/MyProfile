from typing import Optional

from pwdlib import PasswordHash

from . import User, get_user

password_hash = PasswordHash.recommended()


def get_hashed_password(user: User) -> str:
    return password_hash.hash("111")


def verify_password(user: User, password: str) -> Optional[User]:
    return user if password_hash.verify(password, get_hashed_password(user)) else None


def authenticate_user(username: str, password: str) -> Optional[User]:
    return (user := get_user(username)) and verify_password(user, password)
