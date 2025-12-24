from selene import browser

from src.config.browser_new.base_strategy import BrowserStrategy
from src.config.browser_new.chrome_strategy import ChromeStrategy
from src.config.browser_new.firefox_strategy import FirefoxStrategy
from src.config.browser_new.remote_chrome_strategy import RemoteChromeStrategy
from src.config.browser_new.remote_firefox_strategy import RemoteFirefoxStrategy
from src.config.config import CFG


class DriverManager:
    """Driver manager for creating and managing WebDriver instances using Strategy pattern."""

    # Strategy registry
    _STRATEGIES = {
        "chrome": ChromeStrategy,
        "firefox": FirefoxStrategy,
        "remote-chrome": RemoteChromeStrategy,
        "remote-firefox": RemoteFirefoxStrategy,
    }

    def _select_strategy(self) -> BrowserStrategy:
        browser_name = CFG.browser_name.lower()
        strategy_name = (
            browser_name
            if CFG.remote_type.lower() == "none"
            else f"remote_{browser_name}"
        )
        strategy = self._STRATEGIES.get(strategy_name, None)
        if strategy is None:
            raise ValueError(f"Unknown strategy '{strategy_name}'")
        return strategy()

    def init_driver(self) -> None:
        driver = self._select_strategy().create_driver()
        browser.config.base_url = CFG.base_url
        browser.config.timeout = CFG.browser_timeout
        browser.config.save_screenshot_on_failure = True
        browser.config.save_page_source_on_failure = True
        browser.config.driver = driver

    def quit(self) -> None:
        browser.driver.quit()
