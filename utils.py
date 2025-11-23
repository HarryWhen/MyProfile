import functools
from typing import Callable, Mapping, ParamSpec, TypeVar
from urllib.parse import urlencode

T = TypeVar("T")
N = TypeVar("N")
P = ParamSpec("P")


def soft_call(default: N = None) -> Callable[[Callable[P, T]], Callable[P, T | N]]:
    def wrap(func: Callable[P, T]) -> Callable[P, T | N]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T | N:
            try:
                return func(*args, **kwargs)
            except Exception:
                return default

        return wrapper

    return wrap


def create_url(path: str, query: Mapping[str, object]) -> str:
    if not query:
        return path
    return f"{path}?{urlencode(query)}"
