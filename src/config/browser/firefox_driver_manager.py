from typing import List, Dict, Any

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.config.browser.browser_manager import DriverManager
from src.config.config import CFG


class FirefoxDriverManager(DriverManager):

    def create_driver(self) -> Firefox:
        return Firefox(options=self.firefox_options)

    @property
    def firefox_options(self) -> FirefoxOptions:
        options = FirefoxOptions()

        args = self.__headless_args() if CFG.browser_headless else self.__browser_args()
        for arg in args:
            options.add_argument(arg)

        for name, value in self.__browser_prefs().items():
            options.set_preference(name, value)

        return options

    def __browser_args(self) -> List[str]:
        return [
            f"--width={CFG.browser_size[0]}",
            f"--height={CFG.browser_size[1]}",
            "--no-sandbox",
            # "--disable-dev-shm-usage",
        ]

    def __headless_args(self) -> List[str]:
        return [
            "--headless",
            f"--width={CFG.browser_size[0]}",
            f"--height={CFG.browser_size[1]}",
            "--no-sandbox",
            # "--disable-dev-shm-usage",
        ]

    def __browser_prefs(self) -> Dict[str, Any]:
        return {
            "browser.tabs.warnOnClose": False,
            "browser.download.panel.shown": False,
            "browser.download.useDownloadDir": True,
            "browser.helperApps.alwaysAsk.force": False,
            "browser.search.suggest.enabled": False,
            "browser.bookmarks.restore_default_bookmarks": False,
            "signon.rememberSignons": False,
            "signon.autofillForms": False,
            "extensions.formautofill.creditCards.enabled": False,
            "extensions.formautofill.addresses.enabled": False,
            "dom.webnotifications.enabled": False,
            "privacy.donottrackheader.enabled": True,
            "intl.accept_languages": "en,en-US",
        }