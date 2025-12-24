from src.config.browser.chrome_driver_strategy import ChromeDriverStrategy
from src.config.browser.firefox_driver_strategy import FirefoxDriverStrategy
from src.config.browser.remote_chrome_driver_strategy import RemoteChromeDriverStrategy
from src.config.browser.remote_firefox_driver_strategy import (
    RemoteFirefoxDriverStrategy,
)
from src.config.config import CFG


class BrowserManager:

    def init_browser(self) -> None:
        browser_name = CFG.browser_name.lower()
        remote_type = CFG.remote_type.lower()

        if remote_type in ["selenoid", "moon"]:
            match browser_name:
                case "chrome":
                    driver = RemoteChromeDriverStrategy()
                case "firefox":
                    driver = RemoteFirefoxDriverStrategy()
                case _:
                    raise ValueError(f"Unsupported browser: {CFG.browser_name}")
        else:
            match browser_name:
                case "chrome":
                    driver = ChromeDriverStrategy()
                case "firefox":
                    driver = FirefoxDriverStrategy()
                case _:
                    raise ValueError(f"Unsupported browser: {CFG.browser_name}")

        driver.init_driver()
