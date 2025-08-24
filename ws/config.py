import os
from dotenv import load_dotenv

load_dotenv(override=True)


class NeonDBConfig:
    DB_URL = os.environ["NEON_DB_URL"]


class JWTTokenConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]
