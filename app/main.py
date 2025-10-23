from . import app


def run() -> None:
    import os
    from pathlib import Path

    from fastapi_cli.cli import run

    root = Path(__file__).parent.parent
    os.chdir(root)
    run()
