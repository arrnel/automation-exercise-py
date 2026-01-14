from urllib.parse import urlparse

from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.meta.log_level import ApiLogLvl


class MoonApiClient(RestClient):

    def __init__(self):
        parsed_selenoid_url = None if not CFG.remote_url else urlparse(CFG.remote_url)
        if not parsed_selenoid_url:
            raise ValueError("Remote URL must be provided in CFG.remote_url")
        selenoid_domain = f"{parsed_selenoid_url.scheme}://{parsed_selenoid_url.netloc}"
        super().__init__(
            base_url=selenoid_domain,
            follow_redirects=True,
            api_log_lvl=ApiLogLvl.NONE,
        )

    def send_get_video_by_title(
        self,
        video_title: str,
    ) -> AssertableResponse:
        return self.get(url=f"/{video_title}.mp4")
