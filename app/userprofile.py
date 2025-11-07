from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    username: str


class UserProfile(User):
    content: str


def get_user(username: str) -> Optional[User]:
    return User(username=username)


def get_user_profile(user: User) -> UserProfile:
    return UserProfile(
        username=user.username,
        content="I belong to you",
    )
