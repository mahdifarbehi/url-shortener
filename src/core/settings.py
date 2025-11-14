from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://username:password@db:5432/mydb"

    model_config = {
        "env_file": str(Path(__file__).parent.parent.parent / ".env"),
        "env_file_encoding": "utf-8",
    }


settings = Settings()
