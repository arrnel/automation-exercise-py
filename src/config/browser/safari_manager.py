from typing import Dict, Any

from selenium.webdriver import Safari
from selenium.webdriver.safari.options import Options as SafariOptions

from src.config.browser.browser_manager import DriverManager
from src.config.config import CFG


class SafariDriverManager(DriverManager):

    def create_driver(self) -> Safari:
        return Safari(options=self.safari_options)

    @property
    def safari_options(self) -> SafariOptions:
        options = SafariOptions()

        # Safari не поддерживает headless, но если CFG.browser_headless — кидаем soft warning (или игнорируем)
        if CFG.browser_headless:
            print("[WARN] Safari не поддерживает headless режим")

        # Safari Technology Preview если требуется
        if CFG.browser_version.lower() == "tech-preview":
            options.use_technology_preview(True)

        caps = self.__capabilities()
        for k, v in caps.items():
            options.set_capability(k, v)

        return options

    def __capabilities(self) -> Dict[str, Any]:
        return {
            "safari.options.cleanSession": True,
            "safariAllowPopups": False,
            "safariIgnoreFraudWarning": True,
            "autoAcceptAlerts": False,
        }

