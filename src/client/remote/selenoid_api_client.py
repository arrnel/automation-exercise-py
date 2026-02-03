from urllib.parse import urlparse

from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG


class SelenoidApiClient(RestClient):

    def __init__(self):

        if not CFG.remote_url:
            raise RuntimeError(
                f"Remote URL must be provided in CFG.remote_url. Actual value: {CFG.remote_url}"
            )
        parsed_selenoid_url = urlparse(CFG.remote_url)

        super().__init__(
            base_url=f"{parsed_selenoid_url.scheme}://{parsed_selenoid_url.netloc}",
            follow_redirects=True,
            api_log_lvl=CFG.api_log_lvl,
            timeout=15,
        )

    def send_get_file_by_name_request(
        self,
        session_id: str,
        file_name: str,
    ) -> AssertableResponse:
        return self.get(url=f"/download/{session_id}/{file_name}")

    def send_delete_file_by_name_request(
        self,
        session_id: str,
        file_name: str,
    ) -> AssertableResponse:
        return self.delete(url=f"/download/{session_id}/{file_name}")

    def send_get_video_by_title_request(
        self,
        video_title: str,
    ) -> AssertableResponse:
        return self.get(url=f"/video/{video_title}.mp4")

    def send_status_request(
        self,
    ) -> AssertableResponse:
        return self.get(url="/status")
