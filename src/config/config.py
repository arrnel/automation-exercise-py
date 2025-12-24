import ast
import os
from typing import Tuple, Literal, get_args

from pydantic import Field, field_validator, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.model.card import CardInfo
from src.model.enum.meta.log_level import ApiLogLvl, LogLvl
from src.model.enum.meta.user_agent import UserAgent
from src.util.system_util import get_path_in_resources

available_env = Literal["local", "docker", "ci"]


class Settings(BaseSettings):
    # URL
    base_url: str = Field(
        validation_alias="BASE_URL", default="https://automationexercise.com"
    )
    base_api_url: str = Field(
        validation_alias="BASE_API_URL",
        default="/api",
    )

    # BROWSER
    remote_type: str = Field(
        validation_alias=AliasChoices("REMOTE_TYPE"),
        default="none",
    )
    remote_url: str = Field(
        validation_alias=AliasChoices("REMOTE_URL"),
        default="",
    )
    browser_name: str = Field(
        validation_alias=AliasChoices("BROWSER_NAME"),
        default="firefox",
    )
    browser_version: str = Field(
        validation_alias=AliasChoices("BROWSER_VERSION"),
        default="145.0",
    )
    browser_size: Tuple[int, int] = Field(
        validation_alias=AliasChoices("BROWSER_SIZE"),
        default=(1920, 1080),
    )
    browser_headless: bool = Field(
        validation_alias=AliasChoices("BROWSER_HEADLESS"),
        default=False,
    )
    browser_timeout: int = Field(
        validation_alias=AliasChoices("BROWSER_TIMEOUT"),
        default=4,
    )
    browser_page_load_timeout: int = Field(
        validation_alias=AliasChoices("BROWSER_PAGE_LOAD_TIMEOUT"),
        default=10,
    )
    browser_page_load_strategy: str = Field(
        validation_alias=AliasChoices("BROWSER_PAGE_LOAD_STRATEGY"),
        default="eager",
    )
    browser_remote_vnc: bool = Field(
        validation_alias=AliasChoices("BROWSER_REMOTE_VNC"),
        default=True,
    )
    browser_remote_video: bool = Field(
        validation_alias=AliasChoices("BROWSER_REMOTE_VIDEO"),
        default=True,
    )
    browser_remote_logs: bool = Field(
        validation_alias=AliasChoices("BROWSER_REMOTE_LOGS"),
        default=True,
    )
    browser_remote_audio: bool = Field(
        validation_alias=AliasChoices("BROWSER_REMOTE_AUDIO"),
        default=True,
    )
    browser_remote_session_timeout: int = Field(
        validation_alias=AliasChoices("BROWSER_REMOTE_SESSION_TIMEOUT"),
        default=10,
    )
    browser_hold_driver_on_exit: bool = Field(
        validation_alias=AliasChoices("BROWSER_HOLD_DRIVER_ON_EXIT"),
        default=False,
    )

    # API
    default_user_agent: str = Field(
        validation_alias=AliasChoices("DEFAULT_USER_AGENT"),
        default=UserAgent.CHROME_LINUX,
    )
    http_timeout: float = Field(
        validation_alias=AliasChoices("HTTP_TIMEOUT"),
        default=15.0,
    )

    # COOKIES
    csrf_cookie_title: str = Field(default="csrftoken")
    session_id_cookie_title: str = Field(default="sessionid")

    # TEST_DATA
    default_email: str = Field(validation_alias=AliasChoices("DEFAULT_EMAIL"))
    default_password: str = Field(
        validation_alias=AliasChoices("DEFAULT_PASSWORD"),
        default="12345",
    )
    email_domain: str = Field(validation_alias=AliasChoices("EMAIL_DOMAIN"))
    rewrite_all_screenshots: bool = Field(
        validation_alias=AliasChoices("REWRITE_ALL_SCREENSHOTS"),
        default=False,
    )
    default_percent_of_tolerance: float = Field(
        validation_alias=AliasChoices("DEFAULT_PERCENT_OF_TOLERANCE"),
        default=0.0,
    )
    expected_product_id: int = Field(
        validation_alias=AliasChoices("EXPECTED_PRODUCT_ID"),
        default=3,
    )
    expected_products_ids: set[int] = Field(
        validation_alias=AliasChoices("EXPECTED_PRODUCT_IDS"),
        default={1, 2, 3, 5, 8},
    )
    recommended_product_ids: set[int] = Field(
        validation_alias=AliasChoices("RECOMMENDED_PRODUCT_IDS"),
        default={1, 2, 3, 5, 8},
    )
    expected_credit_card: CardInfo = Field(
        validation_alias=AliasChoices("EXPECTED_CREDIT_CARD")
    )

    # LOGGING
    log_lvl: LogLvl = Field(
        validation_alias=AliasChoices("LOG_LVL"),
        default=LogLvl.INFO,
    )
    api_log_lvl: ApiLogLvl = Field(
        validation_alias=AliasChoices("API_LOG_LVL"),
        default=ApiLogLvl.HEADERS,
    )

    # GITHUB
    github_api_url: str = Field(
        validation_alias=AliasChoices("GITHUB_API_URL"),
        default="https://api.github.com",
    )
    github_account_name: str = Field(
        validation_alias=AliasChoices("GITHUB_ACCOUNT_NAME"),
        default="arrnel",
    )
    github_repo_name: str = Field(
        validation_alias=AliasChoices("GITHUB_REPO_NAME"),
        default="automation-exercise-py",
    )
    github_token: str = Field(validation_alias=AliasChoices("GITHUB_TOKEN"))
    github_token_name: str = Field(validation_alias=AliasChoices("GITHUB_TOKEN_NAME"))

    # PYDANTIC
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator(
        "base_url",
        "base_api_url",
        "remote_type",
        "remote_url",
        "browser_name",
        "browser_page_load_strategy",
        "default_email",
        "email_domain",
        mode="before",
    )
    @classmethod
    def lower_case(cls, v: str) -> str:
        if isinstance(v, str):
            return v.lower()
        return v

    @field_validator(
        "log_lvl",
        "api_log_lvl",
        mode="before",
    )
    @classmethod
    def upper_case(cls, v: str) -> str:
        if isinstance(v, str):
            return v.upper()
        return v

    @field_validator("expected_credit_card", mode="before")
    @classmethod
    def parse_expected_credit_card(cls, v) -> CardInfo:
        if isinstance(v, str):
            return ast.literal_eval(v)
        return v

    @field_validator("log_lvl", mode="before")
    @classmethod
    def parse_log_lvl(cls, v):
        if isinstance(v, str) and v in LogLvl.__members__:
            return LogLvl[v]
        return v

    @field_validator("api_log_lvl", mode="before")
    @classmethod
    def parse_api_log_lvl(cls, v):
        if isinstance(v, str) and v in ApiLogLvl.__members__:
            return ApiLogLvl[v]
        return v


def load_settings() -> Settings:
    env = os.getenv("ENV", "local").lower()
    if env not in get_args(available_env):
        raise EnvironmentError(f"Environment {env} not supported.")

    class EnvSettings(Settings):
        model_config = SettingsConfigDict(
            env_file=get_path_in_resources(f"config/.env.{env}"),
            env_file_encoding="utf-8",
            extra="ignore",
            frozen=True,
        )

    return EnvSettings()


def configuration_text() -> str:
    def config_to_str(settings) -> str:
        lines: list[str] = []
        excluded_fields = ["github_token"]

        for field_name, value in settings.__dict__.items():
            if field_name.startswith("_"):
                continue
            if field_name in excluded_fields:
                lines.append(f"{field_name}: {'***' if value else value}")
            else:
                lines.append(f"{field_name}: {value}")

        return "\n".join(lines)

    return f"ENV: '{os.environ.get('ENV')}'\n" + config_to_str(CFG)


CFG = load_settings()
CONFIGURATION_TEXT = configuration_text()
