import ast
import os
from pathlib import Path
from typing import Tuple, Literal, Any

from pydantic import Field, field_validator, AliasChoices
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    DotEnvSettingsSource,
    EnvSettingsSource,
)

from src.model.card import CardInfo
from src.model.enum.meta.log_level import ApiLogLvl, LogLvl
from src.model.enum.meta.user_agent import UserAgent
from src.model.enum.remote_type import RemoteType
from src.util import system_util

_AVAILABLE_ENV = Literal["local", "docker", "ci"]


class NonEmptySettingsSourceMixin(EnvSettingsSource):
    """Source of env vars, which ignore empty env vars"""

    def get_field_value(self, field, field_name: str) -> tuple[Any, str | None, bool]:
        value, key, is_complex = super().get_field_value(field, field_name)

        if isinstance(value, str) and not value.strip():
            return None, None, False

        return value, key, is_complex


class NonEmptyEnvSettingsSource(
    NonEmptySettingsSourceMixin,
    EnvSettingsSource,
):
    pass


class NonEmptyDotEnvSettingsSource(
    NonEmptySettingsSourceMixin,
    DotEnvSettingsSource,
):
    pass


class Settings(BaseSettings):
    # URL
    base_url: str = Field(
        validation_alias="BASE_URL",
        default="https://automationexercise.com",
    )
    base_api_url: str = Field(
        validation_alias="BASE_API_URL",
        default="https://automationexercise.com/api",
    )

    # BROWSER
    remote_type: RemoteType = Field(
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
        default="125.0",
    )
    browser_size: Tuple[int, int] = Field(
        validation_alias=AliasChoices("BROWSER_SIZE"),
        default=(1920, 1080),
    )
    browser_timeout: int = Field(
        validation_alias=AliasChoices("BROWSER_TIMEOUT"),
        default=4,
    )
    browser_scripts_timeout: int = Field(
        validation_alias=AliasChoices("BROWSER_SCRIPTS_TIMEOUT"),
        default=10,
    )
    browser_page_load_timeout: int = Field(
        validation_alias=AliasChoices("BROWSER_PAGE_LOAD_TIMEOUT"),
        default=10,
    )
    browser_page_load_strategy: str = Field(
        validation_alias=AliasChoices("BROWSER_PAGE_LOAD_STRATEGY"),
        default="eager",
    )
    browser_download_dir: str = Field(
        validation_alias=AliasChoices("BROWSER_DOWNLOAD_DIR"),
        default="home/selenium/Downloads",
    )
    browser_override_downloaded_file_dir: str = Field(
        validation_alias=AliasChoices("BROWSER_OVERRIDE_DOWNLOADED_FILE_DIR"),
        default=system_util.get_path_in_resources("files/download"),
    )
    browser_remote_vnc: bool = Field(
        validation_alias=AliasChoices("BROWSER_REMOTE_VNC"),
        default=True,
    )
    browser_remote_video: bool = Field(
        validation_alias=AliasChoices("BROWSER_REMOTE_VIDEO"),
        default=True,
    )
    browser_remote_video_id_type: str = Field(
        validation_alias=AliasChoices("BROWSER_REMOTE_VIDEO_ID_TYPE"),
        default="test_name",
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
    default_screenshot_timeout: float = Field(
        validation_alias=AliasChoices("DEFAULT_SCREENSHOT_TIMEOUT"),
        default=0.1,
    )
    allure_attach_test_artifacts: str = Field(
        validation_alias=AliasChoices("ALLURE_ATTACH_TEST_ARTIFACTS"),
        default="failed",
    )
    allure_attach_test_video: str = Field(
        validation_alias=AliasChoices("ALLURE_ATTACH_TEST_VIDEO"),
        default="failed",
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
    path_to_files: str = Field(
        validation_alias=AliasChoices("PATH_TO_FILES"),
        default=system_util.get_path_in_resources("files/downloads"),
    )
    extension_path: str = Field(
        default=system_util.get_path_in_resources("browser/extension/")
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
        validation_alias=AliasChoices("GH_API_URL"),
        default="https://api.github.com",
    )
    github_account_name: str = Field(
        validation_alias=AliasChoices("GH_ACCOUNT_NAME"),
        default="arrnel",
    )
    github_repo_name: str = Field(
        validation_alias=AliasChoices("GH_REPO_NAME"),
        default="automation-exercise-py",
    )
    github_token: str = Field(validation_alias=AliasChoices("GH_TOKEN"))
    github_token_name: str = Field(validation_alias=AliasChoices("GH_TOKEN_NAME"))

    # PYDANTIC
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @staticmethod
    def is_remote():
        return CFG.remote_type in RemoteType.remote_types()

    @staticmethod
    def is_local():
        return CFG.remote_type not in RemoteType.remote_types()

    @staticmethod
    def is_adblock_enabled():
        match CFG.browser_name:
            case "chrome":
                return float(CFG.browser_version) > 128.0
            case "firefox":
                return float(CFG.browser_version) > 125.0
            case _:
                raise RuntimeError(f"Unknown browser name: {CFG.browser_name}")

    @field_validator(
        "base_url",
        "base_api_url",
        "remote_url",
        "browser_name",
        "browser_remote_video_id_type",
        "browser_page_load_strategy",
        "default_email",
        "allure_attach_test_artifacts",
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

    @field_validator("remote_type", mode="before")
    @classmethod
    def parse_remote_type(cls, v: str) -> RemoteType:
        try:
            return RemoteType(v.lower())
        except ImportError:
            raise ValueError(
                f"Invalid remote type: {v}. Available values: {[rt.value for rt in RemoteType]}"
            )

    @field_validator("path_to_files", mode="before")
    @classmethod
    def relative_resources_folder_path(cls, v: str) -> str:
        folder_path = system_util.get_path_in_resources(v)
        path = Path(folder_path)
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Path should exists and be a directory: {v}")
        return folder_path

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

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        env = os.getenv("ENV", "local").lower()

        custom_env = NonEmptyEnvSettingsSource(settings_cls)

        if env == "ci":
            return (
                init_settings,
                custom_env,
                file_secret_settings,
            )

        env_file_path = system_util.get_path_in_root(f"env/.env.{env}")

        custom_dotenv = NonEmptyDotEnvSettingsSource(
            settings_cls,
            env_file=env_file_path if Path(env_file_path).exists() else None,
            env_file_encoding="utf-8",
        )

        return (
            init_settings,
            custom_env,
            custom_dotenv,
            file_secret_settings,
        )


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

    return f"ENV: '{os.getenv("ENV", "local").lower()}'\n" + config_to_str(CFG)


CFG = Settings()
CFG_TEXT = configuration_text()
