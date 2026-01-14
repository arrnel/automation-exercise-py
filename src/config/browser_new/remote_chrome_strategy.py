from typing import List, override, Dict, Any

from selenium import webdriver

from src.config.browser_new.base_strategy import BrowserStrategy
from src.config.browser_new.capabilities_builder import CapabilitiesBuilder
from src.config.browser_new.chrome_strategy_mixin import ChromeStrategyMixin
from src.config.config import CFG
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


class RemoteChromeStrategy(BrowserStrategy, ChromeStrategyMixin):

    def create_driver(self) -> webdriver.Remote:
        return webdriver.Remote(
            command_executor=CFG.remote_url,
            options=self._build_chrome_options(),
        )

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
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        return {
            "excludeSwitches": ["enable-automation"],
            "useAutomationExtension": False,
            "download.default_directory": f"{CFG.browser_download_dir}/{test_name}",
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            # Autofill
            "profile.default_content_setting_values.notifications": 2,
            "profile.password_manager_enabled": False,
            "credentials_enable_service": False,
            "autofill.profile_enabled": False,
            "autofill.credit_card_enabled": False,
        }

    @override
    def capabilities(self) -> Dict[str, Any]:
        return CapabilitiesBuilder().capabilities()
