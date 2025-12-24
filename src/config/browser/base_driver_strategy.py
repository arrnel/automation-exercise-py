import logging
import os
from abc import ABC, abstractmethod, ABCMeta
from typing import Dict, Any

from selene import browser

from src.config.config import CFG
from src.util import duration_util
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore

_SESSION_TIMEOUT = duration_util.seconds_to_golang_duration_str(
    CFG.browser_remote_session_timeout
)


class DriverStrategy(ABC):

    @abstractmethod
    def _create_driver(self):
        raise NotImplementedError

    def init_driver(self) -> None:
        try:
            driver = self._create_driver()
            driver.implicitly_wait(CFG.browser_timeout)
            driver.set_page_load_timeout(CFG.browser_page_load_timeout)
            driver.set_script_timeout(CFG.browser_page_load_timeout)
            browser.config.driver = driver
            browser.config.save_screenshot_on_failure = True
            browser.config.save_screenshot_on_failure = True
            browser.config.base_url = CFG.base_url
            logging.debug("Driver created")
        except Exception as e:
            logging.error(f"Failed to create driver: {e}")
            raise


class RemoteDriverStrategy(DriverStrategy, metaclass=ABCMeta):

    def _selenoid_options(self) -> Dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        return {
            "name": f"{test_name}",
            "videoName": f"{test_name}.mp4",
            "screenResolution": f"{CFG.browser_size[0]}x{CFG.browser_size[1]}",
            "enableVNC": CFG.browser_remote_vnc,
            "enableLog": CFG.browser_remote_logs,
            "enableVideo": CFG.browser_remote_video,
            "sessionTimeout": _SESSION_TIMEOUT,
            "env": [
                f"ENV={os.environ.get('ENV')}",
            ],
        }

    def _moon_options(self) -> Dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        return {
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
        }
