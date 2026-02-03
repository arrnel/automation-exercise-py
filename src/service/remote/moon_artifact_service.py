from typing import override

from src.client.remote.selenoid_api_client import SelenoidApiClient
from src.service.remote.remote_artifact_service import RemoteArtifactsService
from src.util.decorator.step_logger import step_log


class MoonArtifactApiService(RemoteArtifactsService):

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
        Get file from current test moon container
        Args:
            session_id (str): browser session id.
            file_name (str): title of expected file. Example, "file.txt"
            retries (int): number of retries to get video
            delay (float): timeout before new retry
        """

        raise NotImplementedError()

    @override
    @step_log.log("Delete file [{file_name}] from browser container")
    def delete_file(self, session_id: str, file_name: str) -> None:
        """
        Delete file from current test moon container
        Args:
            session_id (str): browser session id
            file_name (str): file name
        """
        raise NotImplementedError()

    @override
    @step_log.log("Get test video from Moon by video id = [{video_id}]")
    def get_video(
        self,
        video_id: str,
        retries: int = 5,
        delay: float = 2.0,
    ) -> bytes:
        """
        Download a video from Moon
        Args:
            video_id (str): video id - test_title or session_id
            retries (int): number of retries to get video
            delay (float): delay before new retry
        """
        raise NotImplementedError()
