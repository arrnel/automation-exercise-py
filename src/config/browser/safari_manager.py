from selenium.webdriver import Safari, SafariOptions

from src.config.browser.base_browser_options import BrowserStrategy
from src.config.browser.remote_capabilities import RemoteCapabilitiesFactory
from src.config.config import CFG


class SafariStrategy(BrowserStrategy):

    def create_options(self):
        options = SafariOptions()

        if CFG.is_remote:
            capabilities = RemoteCapabilitiesFactory().capabilities()
            for key, value in capabilities:
                options.set_capability(key, value)

        return options

    def create_driver(self, options) -> Safari:
        return Safari()
