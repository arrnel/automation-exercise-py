import os
from typing import Dict, Any

from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.config.browser.browser_manager import DriverManager
from src.config.config import CFG
from src.util.api.test_thread_id_store import ThreadSafeTestThreadsStore
from src.util.duration_util import seconds_to_golang_duration_str

_SESSION_TIMEOUT = seconds_to_golang_duration_str(CFG.browser_remote_session_timeout)

class RemoteDriverManager(DriverManager):

    def create_driver(self) -> Remote:

        if CFG.remote_type.lower() == "selenoid":
            capabilities = self.selenoid_capabilities
        elif CFG.remote_type.lower() == "moon":
            capabilities = self.moon_capabilities
        else:
            raise ValueError(f"Unknown remote type: {CFG.remote_type}")

        return Remote(
            command_executor=CFG.remote_url,
            options=self.browser_options.capabilities(capabilities),
        )

    @property
    def browser_options(self):
        match CFG.browser_name.lower():
            case "chrome":
                return self.chrome_options
            case "firefox":
                return self.firefox_options
            case "safari":
                raise ValueError("Selenoid does not support safari")
            case _:
                raise ValueError(f"Selenoid does not support browser: {CFG.browser_name}")

    @property
    def chrome_options(self):
        options = ChromeOptions()
        options.add_argument(
            f"--window-size={CFG.browser_size[0]},{CFG.browser_size[1]}"
        )
        if CFG.browser_headless:
            options.add_argument("--headless=new")
        options.add_experimental_option(
            "prefs",
            {
                "autofill.credit_card_enabled": False,
                "profile.password_manager_enabled": False,
                "credentials_enable_service": False,
            },
        )
        return options

    @property
    def firefox_options(self):
        options = FirefoxOptions()
        options.add_argument(f"--width={CFG.browser_size[0]}")
        options.add_argument(f"--height={CFG.browser_size[1]}")
        if CFG.browser_headless:
            options.add_argument("--headless")
        options.set_preference("signon.rememberSignons", False)
        options.set_preference("extensions.formautofill.creditCards.enabled", False)

        return options

    @property
    def selenoid_capabilities(self) -> Dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        return {
            "browserName": CFG.browser_name,
            "browserVersion": CFG.browser_version,
            "selenoid:options": {
                "name": f"{test_name}",
                "videoName": f"{test_name}.mp4",
                "screenResolution": f"{CFG.browser_size[0]}x{CFG.browser_size[1]}",
                "enableVNC": CFG.browser_remote_vnc,
                "enableLog": CFG.browser_remote_logs,
                "enableVideo": CFG.browser_remote_video,
                "sessionTimeout": _SESSION_TIMEOUT,
                "env": [
                    f"ENV={os.environ.get('ENV')}",
                ]
            },
        }

    @property
    def moon_capabilities(self) -> Dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        return {
            "browserName": CFG.browser_name,
            "browserVersion": CFG.browser_version,
            "moon:options": {
                "name": f"{test_name}",
                "screenResolution": f"{CFG.browser_size[0]}x{CFG.browser_size[1]}",
                "videoName": f"{test_name}.mp4",
                "enableVideo": CFG.browser_remote_video,
                "enableAudio": CFG.browser_remote_audio,
                "labels": {
                    "project": "ui-tests",
                    "env": "ci",
                },
                "env": [
                    f"ENV={os.environ.get('ENV')}",
                ],
                "logLevel": "INFO",
                "sessionTimeout": _SESSION_TIMEOUT,
            },
        }
