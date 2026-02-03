import os
from typing import Any

from src.config.config import CFG
from src.model.enum.remote_type import RemoteType
from src.util import time_util
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore

_SELENOID_OPTIONS_TITLE = "selenoid:options"
_MOON_OPTIONS_TITLE = "moon:options"


class CapabilitiesBuilder:
    """Build capabilities for local and remote WebDriver instances."""

    def capabilities(self):

        capabilities = self.__local_capabilities()
        if CFG.remote_type == RemoteType.SELENOID:
            capabilities = self.__selenoid_capabilities()
        elif CFG.remote_type == RemoteType.MOON:
            capabilities = self.__moon_capabilities()

        return {**capabilities, **self.__timeout_capabilities()}

    def __local_capabilities(self) -> dict[str, Any]:
        capabilities = {
            "browserName": CFG.browser_name,
            "pageLoadStrategy": CFG.browser_page_load_strategy,
            "unhandledPromptBehavior": "dismiss",
        }
        return capabilities

    def __selenoid_capabilities(self) -> dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        session_timeout = time_util.seconds_to_golang_duration_str(
            CFG.browser_remote_session_timeout
        )

        remote_options = {
            "browserName": CFG.browser_name,
            "browserVersion": CFG.browser_version,
            "pageLoadStrategy": CFG.browser_page_load_strategy,
            "unhandledPromptBehavior": "dismiss",
            _SELENOID_OPTIONS_TITLE: {
                "enableVNC": CFG.browser_remote_vnc,
                "enableVideo": CFG.browser_remote_video,
                "enableLog": CFG.browser_remote_logs,
                "timeZone": "Europe/Moscow",
                "labels": {
                    "env": os.getenv("ENV"),
                    "project": CFG.github_repo_name,
                    "test_name": test_name,
                },
                "sessionTimeout": session_timeout,
            },
        }

        if CFG.browser_remote_video_id_type == "test_name":
            remote_options[_SELENOID_OPTIONS_TITLE]["name"] = test_name
            remote_options[_SELENOID_OPTIONS_TITLE]["logName"] = f"{test_name}.log"
            remote_options[_SELENOID_OPTIONS_TITLE]["videoName"] = f"{test_name}.mp4"

        return remote_options

    def __moon_capabilities(self) -> dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        session_timeout = time_util.seconds_to_golang_duration_str(
            CFG.browser_remote_session_timeout
        )
        remote_options = {
            "browserName": CFG.browser_name,
            "browserVersion": CFG.browser_version,
            "pageLoadStrategy": CFG.browser_page_load_strategy,
            "unhandledPromptBehavior": "dismiss",
            _MOON_OPTIONS_TITLE: {
                "screenResolution": f"{CFG.browser_size[0]}x{CFG.browser_size[1]}",
                "enableVNC": CFG.browser_remote_vnc,
                "enableVideo": CFG.browser_remote_video,
                "enableAudio": CFG.browser_remote_audio,
                "enableHAR": CFG.browser_remote_logs,
                "labels": {
                    "env": os.getenv("ENV"),
                    "project": CFG.github_repo_name,
                    "test_name": test_name,
                },
                "sessionTimeout": session_timeout,
            },
        }

        if CFG.browser_remote_video_id_type == "test_name":
            remote_options[_MOON_OPTIONS_TITLE]["name"] = test_name
            remote_options[_MOON_OPTIONS_TITLE]["videoName"] = f"{test_name}.mp4"

        return remote_options

    @staticmethod
    def __timeout_capabilities() -> dict[str, dict[str, int]]:
        return {
            "timeouts": {
                "implicit": CFG.browser_timeout,
                "pageLoad": CFG.browser_page_load_timeout,
                "script": CFG.browser_scripts_timeout,
            }
        }
