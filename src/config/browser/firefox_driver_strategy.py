from typing import Any

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.config.browser.base_driver_strategy import DriverStrategy
from src.config.config import CFG


class FirefoxDriverStrategy(DriverStrategy):

    def _create_driver(self) -> Firefox:
        return Firefox(options=self.firefox_options)

    @property
    def firefox_options(self) -> FirefoxOptions:
        options = FirefoxOptions()
        args = self.__headless_args() if CFG.browser_headless else self.__browser_args()
        for arg in args:
            options.add_argument(arg)
        for k, v in self.__browser_prefs().items():
            options.set_preference(k, v)

        options.set_capability("browserVersion", CFG.browser_version)
        options.set_capability("pageLoadStrategy", CFG.browser_page_load_strategy)
        options.set_capability("timeouts", {"implicit": CFG.browser_timeout})
        return options

    def __browser_args(self) -> list[str]:
        return [
            f"--width={CFG.browser_size[0]}",
            f"--height={CFG.browser_size[1]}",
            "--no-sandbox",
        ]

    def __headless_args(self) -> list[str]:
        return [
            "--headless",
            f"--width={CFG.browser_size[0]}",
            f"--height={CFG.browser_size[1]}",
            "--no-sandbox",
        ]

    def __browser_prefs(self) -> dict[str, Any]:
        return {
            "browser.tabs.warnOnClose": False,
            "browser.download.useDownloadDir": True,
            "signon.rememberSignons": False,
            "extensions.formautofill.creditCards.enabled": False,
            "dom.webnotifications.enabled": False,
            "intl.accept_languages": "en,en-US",
        }
