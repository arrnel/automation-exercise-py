from typing import List, override, Dict, Any

from selenium import webdriver

from src.browser.base_strategy import BrowserStrategy
from src.browser.capability_builder import CapabilitiesBuilder
from src.browser.firefox_strategy_mixin import FirefoxStrategyMixin
from src.config.config import CFG


class RemoteFirefoxStrategy(BrowserStrategy, FirefoxStrategyMixin):

    @override
    def create_driver(self) -> webdriver.Remote:
        options = self._build_firefox_options()
        options.enable_downloads = True
        return webdriver.Remote(
            command_executor=CFG.remote_url,
            options=options,
        )

    @override
    def firefox_args(self) -> List[str]:
        width, height = CFG.browser_size[0], CFG.browser_size[1]
        args = [
            f"--width={width}",
            f"--height={height}",
            "--disable-dev-shm-usage",
        ]
        if CFG.browser_headless:
            args.append("--headless")
        return args

    @override
    def firefox_prefs(self) -> Dict[str, Any]:
        return {
            "pdfjs.disabled": True,
            "browser.download.folderList": 2,
            "browser.download.dir": f"{CFG.browser_download_dir}",
            "browser.download.manager.showWhenStarting": False,
            "browser.download.panel.shown": False,
            "dom.webdriver.enabled": False,
            "useAutomationExtension": False,
            "media.webspeech.synth.enabled": False,
            "media.webspeech.recognition.enable": False,
        }

    @override
    def capabilities(self) -> Dict[str, Any]:
        return CapabilitiesBuilder().capabilities()
