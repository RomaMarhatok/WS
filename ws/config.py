import os
from dotenv import load_dotenv

load_dotenv(override=True)

print(os.environ)


class NeonDBConfig:
    DB_URL = os.environ["NEON_DB_URL"]
