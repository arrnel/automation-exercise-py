import os
from typing import Any

from src.config.config import CFG
from src.util import duration_util
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore


class CapabilitiesBuilder:
    """Build capabilities for local and remote WebDriver instances."""

    def capabilities(self):
        capabilities = self.__local_capabilities()
        capabilities["timeouts"] = self.__timeout_capabilities()
        if CFG.remote_type == "selenoid":
            capabilities["selenoid:options"] = self.__selenoid_capabilities()
        elif CFG.remote_type == "moon":
            capabilities["moon:options"] = self.__moon_capabilities()
        return capabilities

    def __local_capabilities(self) -> dict[str, Any]:
        capabilities = {
            "browserName": CFG.browser_name,
            "pageLoadStrategy": CFG.browser_page_load_strategy,
            "unhandledPromptBehavior": "dismiss",
        }
        return capabilities

    def __selenoid_capabilities(self) -> dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        session_timeout = duration_util.seconds_to_golang_duration_str(
            CFG.browser_remote_session_timeout
        )

        selenoid_data = {
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
        }

        if CFG.browser_remote_video_id_type == "test_name":
            selenoid_data["name"] = test_name
            selenoid_data["logName"] = f"{test_name}.log"
            selenoid_data["videoName"] = f"{test_name}.mp4"

        return selenoid_data

    def __moon_capabilities(self) -> dict[str, Any]:
        test_name = ThreadSafeTestThreadsStore().current_thread_test_name()
        session_timeout = duration_util.seconds_to_golang_duration_str(
            CFG.browser_remote_session_timeout
        )
        return {
            "name": test_name,
            "videoName": f"{test_name}.mp4",
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
        }

    @staticmethod
    def __timeout_capabilities() -> dict[str, int]:
        return {
            "implicit": CFG.browser_timeout,
            "pageLoad": CFG.browser_page_load_timeout,
            "script": CFG.browser_page_load_timeout,
        }
