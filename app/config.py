from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path
from typing import List

import os

load_dotenv(str(Path(__file__).parent.parent / ".env"))


class Settings(BaseSettings):
    # DATABASE
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_NAME: str = os.environ.get("DB_NAME", "")
    DB_USER: str = os.environ.get("DB_USER", "")
    DB_PORT: int = int(os.environ.get("DB_PORT", "5432"))
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")

    # CORS ORIGINS
    CORS_ORIGINS: List[str] = ["*"]

    DEBUG: bool = True

    # SECURITY
    BCRYPT_ROUNDS: int = 5


settings: Settings = Settings()
