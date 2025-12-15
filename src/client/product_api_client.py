from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.meta.content_type import ContentType
from src.util.api.routes import ApiRoutes


class ProductApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.base_api_url,
            content_type=ContentType.URL_ENCODED
        )

    def send_search_products_by_query_request(self, query: str) -> AssertableResponse:
        return self.post(
            url=ApiRoutes.SEARCH_PRODUCTS.path(),
            data={
                "search_product": query,
            },
        )

    def send_get_all_products_request(self) -> AssertableResponse:
        return self.get(ApiRoutes.PRODUCTS_LIST.path())
