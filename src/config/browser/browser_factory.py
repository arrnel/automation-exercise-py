from abc import ABC, abstractmethod

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Safari, SafariOptions

from src.config.browser.chrome_options import ChromeStrategy
from src.config.browser.firefox_options import FirefoxStrategy
from src.config.browser.remote_capabilities import RemoteCapabilitiesFactory
from src.config.browser.safari_options import SafariStrategy
from src.config.config import CFG


class BrowserFactory:

    def get_browser(self) -> "BrowserStrategy":
        match (CFG.browser_name.lower()):
            case "chrome":
                return ChromeStrategy()
            case "firefox":
                return FirefoxStrategy()
            case "safari":
                return SafariStrategy()
            case _:
                raise ValueError(f"Unsupported browser: {CFG.browser_name}")
