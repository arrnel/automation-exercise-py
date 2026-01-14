from typing import Any

from selenium.webdriver import Chrome, ChromeOptions

from src.config.browser.base_driver_strategy import DriverStrategy
from src.config.config import CFG
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


class ChromeDriverStrategy(DriverStrategy):

    def _create_driver(self) -> Chrome:
        return Chrome(options=self.chrome_options)

    @property
    def chrome_options(self) -> ChromeOptions:
        options = ChromeOptions()
        options.page_load_strategy = CFG.browser_page_load_strategy
        options.set_capability("timeouts", {"implicit": CFG.browser_timeout})
        options.set_capability("browserVersion", CFG.browser_version)

        args = (
            self.__browser_headless_args()
            if CFG.browser_headless
            else self.__browser_args()
        )
        for arg in args:
            options.add_argument(arg)

        options.add_experimental_option("prefs", self.__experimental_options())
        return options

    def __browser_args(self) -> list[str]:
        return [
            f"--window-size={CFG.browser_size[0]},{CFG.browser_size[1]}",
            "--disable-features=PrivacySandboxSettings3",
            "--disable-features=UserAgentClientHint",
            "--disable-features=CookieDeprecationMessages",
            "--disable-features=InterestCohortAPI",
            "--disable-features=SameSiteByDefaultCookies",
            "--disable-popup-blocking",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-notifications",
        ]

    def __browser_headless_args(self) -> list[str]:
        return [
            "--headless=new",
            "--disable-gpu",
            f"--window-size={CFG.browser_size[0]},{CFG.browser_size[1]}",
            "--disable-features=PrivacySandboxSettings3",
            "--disable-features=UserAgentClientHint",
            "--disable-features=CookieDeprecationMessages",
            "--disable-features=InterestCohortAPI",
            "--disable-features=SameSiteByDefaultCookies",
            "--disable-popup-blocking",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-infobars",
            "--disable-notifications",
        ]

    def __experimental_options(self) -> dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        return {
            "autofill.credit_card_enabled": False,
            "autofill.profile_enabled": False,
            "download.default_directory": f"{CFG.browser_download_dir}/{test_name}",
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "intl.accept_languages": "en,en_US",
        }
