from typing import List, override, Dict, Any

from selenium import webdriver

from src.browser.base_strategy import BrowserStrategy
from src.browser.capability_builder import CapabilitiesBuilder
from src.browser.chrome_strategy_mixin import ChromeStrategyMixin
from src.config.config import CFG
from src.util import system_util
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


class ChromeStrategy(BrowserStrategy, ChromeStrategyMixin):

    @override
    def create_driver(self) -> webdriver.Chrome:
        options = self._build_chrome_options()
        options.enable_downloads = True
        return webdriver.Chrome(options=options)

    @override
    def chrome_args(self) -> List[str]:
        width, height = CFG.browser_size[0], CFG.browser_size[1]
        args = [
            f"--window-size={width},{height}",
            "--disable-dev-shm-usage",
            "--disable-gpu",
        ]
        return args

    @override
    def chrome_extensions(self) -> List[str]:
        all_extensions: List[str] = [
            "ublock/ublock.crx",
        ]
        return [CFG.extension_path + extension for extension in all_extensions]

    @override
    def chrome_experimental_options(self) -> Dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        download_dir = f"{CFG.browser_download_dir}/{test_name}"
        return {
            # Download
            "download.default_directory": download_dir,
            "savefile.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            # Autofill
            "credentials_enable_service": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
            # Profile
            "profile.default_content_setting_values.automatic_downloads": True,
            "profile.default_content_setting_values.notifications": 2,
            "profile.password_manager_enabled": False,
            # Safe-browsing
            "safebrowsing_for_trusted_sources_enabled": False,
            "safebrowsing.enabled": False,
        }

    @override
    def capabilities(self) -> Dict[str, Any]:
        return CapabilitiesBuilder().capabilities()
