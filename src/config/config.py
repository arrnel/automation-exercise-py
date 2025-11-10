import os
from typing import Tuple, Literal, get_args

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.model.enum.log_level import ApiLogLvl, LogLvl
from src.model.enum.user_agent import UserAgent
from src.util.system_util import get_path_in_resources

available_env = Literal["local", "docker", "ci"]


class Settings(BaseSettings):

    # URL
    base_url: str = Field(default="https://automationexercise.com")
    base_api_url: str = Field(default="/api")

    # BROWSER
    is_remote: bool = Field(default=False)
    remote_url: str = Field(default="")
    browser_name: str = Field(default="chrome")
    browser_version: str = Field(default="139.0")
    browser_size: Tuple[int, int] = Field(default=(1920, 1080))
    browser_headless: bool = Field(default=False)
    browser_timeout: int = Field(default=4)
    browser_page_load_timeout: int = Field(default=10)
    browser_hold_driver_on_exit: bool = Field(default=False)

    # API
    default_user_agent: str = Field(default=UserAgent.CHROME_LINUX)
    http_timeout: float = Field(default=15.0)

    # COOKIES
    csrf_cookie_title: str = Field(default="csrftoken")
    session_id_cookie_title: str = Field(default="sessionid")

    # TEST DATA
    default_password: str = Field(default="12345")
    email_domain: str = Field()

    # LOGGING
    log_lvl: LogLvl = Field(default=LogLvl.INFO)
    api_log_lvl: ApiLogLvl = Field(default=ApiLogLvl.HEADERS)

    # GITHUB
    github_api_url: str = Field(default="https://api.github.com")
    github_account_name: str = Field(default="arrnel")
    github_repo_name: str = Field(default="automation-exercise-python")
    github_token: str = Field()
    github_token_name: str = Field()

    # PYDANTIC
    model_config = SettingsConfigDict(env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="before")
    @classmethod
    def parse_browser_size(cls, values: dict) -> dict:
        separators = ("x", ",", " ")
        val = values.get("browser_size").strip()
        if val is None:
            return values
        if isinstance(val, str):
            for sep in separators:
                if sep in val:
                    try:
                        width, height = map(int, val.split(sep))
                        values["browser_size"] = (width, height)
                        return values
                    except ValueError:
                        raise ValueError(f"Неверный формат browser_size: {val}")
        return values


def load_settings() -> Settings:

    env = os.getenv("ENV", "local")
    if env.lower() not in get_args(available_env):
        raise EnvironmentError(f"Environment {env} not supported.")

    # Настройки с указанием файла .env
    class EnvSettings(Settings):
        model_config = SettingsConfigDict(
            env_file=get_path_in_resources(f"config/.env.{env}"),
            env_file_encoding="utf-8",
            extra="ignore",
        )

    return EnvSettings()


# === Глобальный доступ ===
CFG = load_settings()
