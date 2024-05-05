import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    base_url: str = "https://exponent.run"
    base_api_url: str = "https://api.exponent.run"
    api_key: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="EXPONENT_",
        env_file=os.path.expanduser("~/.exponent"),
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
