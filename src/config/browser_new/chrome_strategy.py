from typing import List, override, Dict, Any

from selenium import webdriver

from src.config.browser_new.base_strategy import BrowserStrategy
from src.config.browser_new.capabilities_builder import CapabilitiesBuilder
from src.config.browser_new.chrome_strategy_mixin import ChromeStrategyMixin
from src.config.config import CFG


class ChromeStrategy(BrowserStrategy, ChromeStrategyMixin):

    def create_driver(self) -> webdriver.Chrome:
        return webdriver.Chrome(options=self._build_chrome_options())

    @override
    def chrome_args(self) -> List[str]:
        width, height = CFG.browser_size[0], CFG.browser_size[1]
        args = [
            f"--window-size={width},{height}",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-blink-features=AutomationControlled",
        ]
        if CFG.browser_headless:
            args.append("--headless")
        return args

    @override
    def chrome_experimental_options(self) -> Dict[str, Any]:
        return {
            "excludeSwitches": ["enable-automation"],
            "useAutomationExtension": False,
        }

    @override
    def capabilities(self) -> Dict[str, Any]:
        return CapabilitiesBuilder().capabilities()
