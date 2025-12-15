from src.config.browser.browser_manager import DriverManager
from src.config.browser.chrome_driver_manager import ChromeDriverManager
from src.config.browser.firefox_driver_manager import FirefoxDriverManager
from src.config.browser.remote_driver_manager import RemoteDriverManager
from src.config.browser.safari_manager import SafariDriverManager
from src.config.config import CFG


class BrowserFactory:

    @property
    def browser(self) -> DriverManager:

        if CFG.remote_type.lower() in ["selenoid", "moon"]:
            return RemoteDriverManager()

        match (CFG.browser_name.lower()):
            case "chrome":
                return ChromeDriverManager()
            case "firefox":
                return FirefoxDriverManager()
            case "safari":
                return SafariDriverManager()
            case _:
                raise ValueError(f"Unsupported browser: {CFG.browser_name}")
