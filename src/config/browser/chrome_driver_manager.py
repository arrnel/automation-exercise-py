from abc import ABC, abstractmethod
from typing import Any, Dict, List, Set

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Safari, SafariOptions

from src.config.browser.browser_manager import DriverManager
from src.config.browser.remote_capabilities import RemoteCapabilitiesFactory
from src.config.config import CFG


class ChromeDriverManager(DriverManager):

    def create_options(self):
        options = ChromeOptions()

        args = self.__browser_headless_args() if CFG.browser_headless else self.__browser_args()
        for arg in args:
            options.add_argument(arg)
        options.add_experimental_option("prefs", self.__experimental_options())

        return options

    def __browser_args(self) -> List[str]:
        return [
            f"--window-size={CFG.browser_size[0]},{CFG.browser_size[1]}"
            "--disable-features=PrivacySandboxSettings3"
            "--disable-features=UserAgentClientHint"
            "--disable-features=CookieDeprecationMessages"
            "--disable-features=InterestCohortAPI"
            "--disable-features=SameSiteByDefaultCookies"
            "--disable-popup-blocking"
            "--no-sandbox"
            "--disable-dev-shm-usage"
            "--disable-infobars"
            "--disable-notifications"
        ]

    def __browser_headless_args(self) -> List[str]:
        return [
            "--headless=new"
            "--disable-gpu"
            f"--window-size={CFG.browser_size[0]},{CFG.browser_size[1]}"
            "--disable-features=PrivacySandboxSettings3"
            "--disable-features=UserAgentClientHint"
            "--disable-features=CookieDeprecationMessages"
            "--disable-features=InterestCohortAPI"
            "--disable-features=SameSiteByDefaultCookies"
            "--disable-popup-blocking"
            "--no-sandbox"
            "--disable-dev-shm-usage"
            "--disable-infobars"
            "--disable-notifications"
        ]

    def __experimental_options(self) -> Dict[str, Any]:
        return {
            "autofill.credit_card_enabled": False,
            "autofill.profile_enabled": False,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "intl.accept_languages": "en,en_US",
        }

    def create_driver(self, options) -> Chrome:
        return Chrome(options=options)
