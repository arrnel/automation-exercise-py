import time
from http import HTTPStatus

from src.client.remote.selenoid_api_client import SelenoidApiClient
from src.ex.exception import SelenoidVideoNotFoundError


class SelenoidApiService:

    def __init__(self):
        self.selenoid_api_client = SelenoidApiClient()

    def get_video(self, video_id: str, retries=5, timeout=2):
        """
        Download a video from Selenoid
        Args:
            video_id (str): video id - test_title or session_id
            retries (int): number of retries to get video
            timeout (int): timeout before new retry
        """
        status_code = 0
        for _ in range(retries):
            response = self.selenoid_api_client.send_get_video_by_title(video_id)
            status_code = response.extract().status_code()
            if status_code == HTTPStatus.OK:
                return response.extract().content_as_bytes()
            time.sleep(timeout)

        raise SelenoidVideoNotFoundError(
            f"Not found video by video_id = {video_id}. "
            f"Response code: {status_code}"
        )
