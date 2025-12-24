from typing import Any

from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions

from src.config.browser.base_driver_strategy import RemoteDriverStrategy
from src.config.config import CFG
from src.util.duration_util import seconds_to_golang_duration_str

_SESSION_TIMEOUT = seconds_to_golang_duration_str(CFG.browser_remote_session_timeout)


class RemoteChromeDriverStrategy(RemoteDriverStrategy):

    def _create_driver(self) -> Remote:
        options = self.chrome_options
        return Remote(
            command_executor=CFG.remote_url,
            options=options,
        )

    @property
    def chrome_options(self) -> ChromeOptions:
        options = ChromeOptions()
        options.page_load_strategy = CFG.browser_page_load_strategy
        options.set_capability("browserVersion", CFG.browser_version)
        options.set_capability(
            "timeouts",
            {
                "implicit": CFG.browser_timeout,
                "pageLoad": CFG.browser_page_load_timeout,
                "script": CFG.browser_page_load_timeout,
            },
        )

        for arg in self._browser_args():
            options.add_argument(arg)

        options.add_experimental_option(
            "prefs",
            self._experimental_options(),
        )
        options.set_capability("browserName", CFG.browser_name)
        options.set_capability("browserVersion", CFG.browser_version)
        self._apply_remote_capabilities(options)
        return options

    def _browser_args(self) -> list[str]:
        args = [
            f"--window-size={CFG.browser_size[0]},{CFG.browser_size[1]}",
            "--disable-features=PrivacySandboxSettings3",
            "--disable-features=UserAgentClientHint",
            "--disable-features=CookieDeprecationMessages",
            "--disable-features=InterestCohortAPI",
            "--disable-features=SameSiteByDefaultCookies",
            "--disable-popup-blocking",
            "--disable-infobars",
            "--disable-notifications",
            "--disable-dev-shm-usage",
            "--no-sandbox",
        ]

        if CFG.browser_headless:
            args.extend(
                [
                    "--headless=new",
                    "--disable-gpu",
                ]
            )

        return args

    def _experimental_options(self) -> dict[str, Any]:
        return {
            "autofill.credit_card_enabled": False,
            "autofill.profile_enabled": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.geolocation": 2,
            "intl.accept_languages": "en,en_US",
        }

    def _apply_remote_capabilities(self, options: ChromeOptions) -> None:
        if CFG.remote_type == "selenoid":
            options.set_capability("selenoid:options", self._selenoid_options())
        elif CFG.remote_type == "moon":
            options.set_capability("moon:options", self._moon_options())
