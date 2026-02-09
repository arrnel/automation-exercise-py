from typing import List, override, Dict, Any

from selenium import webdriver

from src.browser.base_strategy import BrowserStrategy
from src.browser.capability_builder import CapabilitiesBuilder
from src.browser.firefox_strategy_mixin import FirefoxStrategyMixin
from src.config.config import CFG
from src.util import system_util
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


class FirefoxStrategy(BrowserStrategy, FirefoxStrategyMixin):

    @override
    def create_driver(self) -> webdriver.Firefox:
        options = self._build_firefox_options()
        options.enable_downloads = True
        firefox_driver = webdriver.Firefox(options=options)
        self._install_extensions(firefox_driver)
        return firefox_driver

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
    def firefox_extensions(self) -> List[str]:
        all_extensions: List[str] = [
            "ublock/ublock.xpi",
        ]
        return [CFG.extension_path + extension for extension in all_extensions]

    @override
    def capabilities(self) -> Dict[str, Any]:
        return CapabilitiesBuilder().capabilities()
