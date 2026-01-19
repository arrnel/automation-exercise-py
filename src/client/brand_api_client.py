from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.meta.content_type import ContentType
from src.util.api.routes import ApiRoutes


class BrandApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.base_api_url,
            content_type=ContentType.JSON,
            follow_redirects=True,
            timeout=CFG.http_timeout,
        )

    def send_get_all_brands_request(self) -> AssertableResponse:
        return self.get(ApiRoutes.BRANDS_LIST.path())
