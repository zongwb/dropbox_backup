"""Global settings"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):   # pylint: disable=too-few-public-methods
    """Global settings"""

    dropbox_app_key: str = Field(default=..., min_length=3)
    dropbox_app_secret: str = Field(default=..., min_length=3)
    dropbox_refresh_token: str = Field(default=..., min_length=3)
    folder_name: str = Field(default=..., min_length=1)

    class Config:   # pylint: disable=missing-class-docstring,too-few-public-methods
        env_file = '.env'


settings = Settings()
