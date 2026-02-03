from selene import browser

from src.browser.base_strategy import BrowserStrategy
from src.browser.chrome_strategy import ChromeStrategy
from src.browser.firefox_strategy import FirefoxStrategy
from src.browser.remote_chrome_strategy import RemoteChromeStrategy
from src.browser.remote_firefox_strategy import RemoteFirefoxStrategy
from src.config.config import CFG


class DriverManager:
    """Driver manager for creating and managing WebDriver instances using Strategy pattern."""

    # Strategy registry
    _STRATEGIES = {
        "chrome": ChromeStrategy,
        "firefox": FirefoxStrategy,
        "remote_chrome": RemoteChromeStrategy,
        "remote_firefox": RemoteFirefoxStrategy,
    }

    def init_driver(self) -> None:
        driver = self._select_strategy().create_driver()
        driver.implicitly_wait(CFG.browser_timeout)
        driver.set_page_load_timeout(CFG.browser_page_load_timeout)
        driver.set_script_timeout(CFG.browser_scripts_timeout)
        browser.config.driver = driver
        browser.config.base_url = CFG.base_url
        browser.config.save_screenshot_on_failure = True
        browser.config.save_page_source_on_failure = True

    def quit(self) -> None:
        if browser.driver:
            browser.driver.quit()

    def _select_strategy(self) -> BrowserStrategy:
        browser_name = CFG.browser_name.lower()
        strategy_name = browser_name if CFG.is_local() else f"remote_{browser_name}"
        strategy = self._STRATEGIES.get(strategy_name, None)
        if strategy is None:
            raise ValueError(f"Unknown strategy '{strategy_name}'")
        return strategy()
