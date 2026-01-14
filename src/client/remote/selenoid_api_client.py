from urllib.parse import urlparse

from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.meta.log_level import ApiLogLvl


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
            api_log_lvl=ApiLogLvl.NONE,
            timeout=15,
        )

    def send_get_video_by_title(
        self,
        video_title: str,
    ) -> AssertableResponse:
        return self.get(url=f"/video/{video_title}.mp4")
