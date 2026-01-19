import time
from http import HTTPStatus
from typing import override

from src.client.core.condition.conditions import Conditions
from src.client.remote.selenoid_api_client import SelenoidApiClient
from src.config.config import CFG
from src.ex.exception import (
    SelenoidError,
    RemoteFileNotFoundError,
    RemoteVideoNotFoundError,
)
from src.service.remote.remote_artifact_service import RemoteArtifactsService
from src.util import retry_util
from src.util.decorator.step_logger import step_log


class SelenoidArtifactApiService(RemoteArtifactsService):

    def __init__(self):
        self.selenoid_api_client = SelenoidApiClient()

    @override
    @step_log.log("Get file [{file_name}] from browser container")
    def get_file(
        self,
        session_id: str,
        file_name: str,
        retries: int = 5,
        delay: float = 1.0,
    ) -> bytes:
        """
        Get file from current test selenoid container
        Args:
            session_id (str): browser session id.
            file_name (str): title of expected file. Example, "file.txt"
            retries (int): number of retries to get video
            delay (float): timeout before new retry
        """

        def action():
            response = self.selenoid_api_client.send_get_file_by_name_request(
                session_id=session_id,
                file_name=file_name,
            )
            status_code = response.extract().status_code()
            if status_code == HTTPStatus.OK:
                return response.extract().content_as_bytes()
            time.sleep(delay)

            raise RemoteFileNotFoundError(
                f"Not found file by file name = {file_name}. "
                f"Response code: {status_code}"
            )

        return retry_util.retry(
            action=action,
            retries=retries,
            delay=delay,
            error_factory=lambda exc: RemoteFileNotFoundError(
                f"Unable to download file by file name = [{file_name}] after {retries} retries"
            ),
        )

    @override
    @step_log.log("Delete file [{file_name}] from browser container")
    def delete_file(self, session_id: str, file_name: str) -> None:
        """
        Delete file from current test selenoid container
        Args:
            session_id (str): browser session id.
            file_name (str): title of expected file. Example, "file.txt"
        """
        response = self.selenoid_api_client.send_delete_file_by_name_request(
            session_id=session_id, file_name=file_name
        )

        status_code = response.extract().status_code()
        if status_code != HTTPStatus.OK:
            raise RemoteFileNotFoundError(
                f"Unable to delete file by name = [{file_name}]"
            )

    @override
    @step_log.log("Get test video from Selenoid by video id = [{video_id}]")
    def get_video(
        self,
        video_id: str,
        retries: int = 5,
        delay: float = 2.0,
    ) -> bytes:
        """
        Download a video from Selenoid
        Args:
            video_id (str): video id - test_title or session_id
            retries (int): number of retries to get video
            delay (float): timeout before new retry
        """

        def action():
            response = self.selenoid_api_client.send_get_video_by_title_request(
                video_id
            )
            status_code = response.extract().status_code()
            if status_code == HTTPStatus.OK:
                return response.extract().content_as_bytes()
            time.sleep(delay)

            raise SelenoidError(
                f"Not found video by video_id = {video_id}. "
                f"Response code: {status_code}"
            )

        return retry_util.retry(
            action=action,
            retries=retries,
            delay=delay,
            error_factory=lambda exc: RemoteVideoNotFoundError(
                f"Unable to download selenoid video by id = [{video_id}] after {retries} retries"
            ),
        )

    def get_container_id(self, session_id: str) -> str:
        platform_title = "unknown"
        body = (
            self.selenoid_api_client.send_status_request()
            .check(Conditions.status_code(HTTPStatus.OK))
            .extract()
            .as_json()
        )

        sessions = (
            body.get("browsers", {})
            .get(CFG.browser_name, {})
            .get(CFG.browser_version, {})
            .get(platform_title, {})
            .get("sessions", [])
        )

        for session in sessions:
            if session.get("id") == session_id:
                return session.get("container")

        raise SelenoidError(f"Not found container id by session id: {session_id}")
