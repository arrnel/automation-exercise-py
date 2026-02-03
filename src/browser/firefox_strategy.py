from typing import List, override, Dict, Any

from selenium import webdriver

from src.browser.base_strategy import BrowserStrategy
from src.browser.capability_builder import CapabilitiesBuilder
from src.browser.firefox_strategy_mixin import FirefoxStrategyMixin
from src.config.config import CFG
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


class FirefoxStrategy(BrowserStrategy, FirefoxStrategyMixin):

    @override
    def create_driver(self) -> webdriver.Firefox:
        options = self._build_firefox_options()
        options.enable_downloads = True
        return webdriver.Firefox(options=options)

    @override
    def firefox_args(self) -> List[str]:
        width, height = CFG.browser_size[0], CFG.browser_size[1]
        args = [
            f"--width={width}",
            f"--height={height}",
            "--disable-notifications",
            "--disable-infobars",
            "--disable-gpu",
            "--disable-dev-shm-usage",
        ]
        if CFG.browser_headless:
            args.append("--headless")
        return args

    @override
    def firefox_prefs(self) -> Dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        return {
            "pdfjs.disabled": True,
            "browser.download.folderList": 2,
            "browser.download.dir": f"{CFG.browser_download_dir}/{test_name}",
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
