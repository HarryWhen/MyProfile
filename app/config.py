import os
from datetime import timedelta
from pathlib import Path

import dotenv

dotenv.load_dotenv()


TEMPLATES_DIRECTORY = Path(os.environ["TEMPLATES_DIRECTORY"])
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_DELTA = timedelta(
    minutes=int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
)
