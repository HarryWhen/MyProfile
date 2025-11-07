from . import app
from .auth import router as auth
from .profile import router as profile

app.include_router(auth)
app.include_router(profile)


def run() -> None:
    import os
    from pathlib import Path

    from fastapi_cli.cli import run

    root = Path(__file__).parent.parent
    os.chdir(root)
    run()
