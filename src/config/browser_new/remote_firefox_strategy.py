from typing import List, override, Dict, Any

from selenium import webdriver

from src.config.browser_new.base_strategy import BrowserStrategy
from src.config.browser_new.capabilities_builder import CapabilitiesBuilder
from src.config.browser_new.firefox_strategy_mixin import FirefoxStrategyMixin
from src.config.config import CFG


class RemoteFirefoxStrategy(BrowserStrategy, FirefoxStrategyMixin):

    def create_driver(self) -> webdriver.Remote:
        return webdriver.Remote(
            command_executor=CFG.remote_url,
            options=self._build_firefox_options(),
        )

    @override
    def firefox_args(self) -> List[str]:
        width, height = CFG.browser_size[0], CFG.browser_size[1]
        args = [
            f"--window-size={width},{height}",
            "--disable-dev-shm-usage",
        ]
        if CFG.browser_headless:
            args.append("--headless")
        return args

    @override
    def firefox_prefs(self) -> Dict[str, Any]:
        return {
            "dom.webdriver.enabled": False,
            "useAutomationExtension": False,
            "media.webspeech.synth.enabled": False,
            "media.webspeech.recognition.enable": False,
        }

    @override
    def capabilities(self) -> Dict[str, Any]:
        return CapabilitiesBuilder().capabilities()
