from abc import ABC, abstractmethod

from selenium.webdriver import Chrome, ChromeOptions, Firefox, FirefoxOptions, Safari, SafariOptions

from src.config.browser.browser_manager import DriverManager
from src.config.browser.remote_capabilities import RemoteCapabilitiesFactory
from src.config.config import CFG


class FirefoxDriverManager(DriverManager):

    def create_options(self):
        options = FirefoxOptions()

        print(f"FIREFOX: SHOW DEFAULT CAPABILITIES: {options.default_capabilities}")
        print(f"FIREFOX: SHOW CAPABILITIES: {options.capabilities}")
        print(f"FIREFOX: SHOW PREFERENCES: {options.preferences}")
        print(f"FIREFOX: SHOW ARGUMENTS: {options.arguments}")

        if CFG.browser_headless:
            options.add_argument("-headless")

        if CFG.is_remote:
            capabilities = RemoteCapabilitiesFactory().capabilities()
            for key, value in capabilities:
                options.set_capability(key, value)

        options.set_preference("dom.webnotifications.enabled", False)
        options.set_preference("dom.push.enabled", False)
        options.set_preference("extensions.formautofill.creditCards.enabled", False)
        options.set_preference("extensions.formautofill.available", "off")
        options.set_preference("extensions.formautofill.addresses.enabled", False)
        options.set_preference("signon.rememberSignons", False)

        return options

    def create_driver(self, options) -> Firefox:
        return Firefox(options=options)