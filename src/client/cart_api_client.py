from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.meta.content_type import ContentType
from src.util.api.routes import ApiRoutes


class CartApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.base_url,
            follow_redirects=True,
            content_type=ContentType.URL_ENCODED,
            api_log_lvl=CFG.api_log_lvl,
        )

    def add_product_to_cart(self, product_id: int, quantity: int) -> AssertableResponse:
        params = {
            "quantity": quantity,
        }
        return self.get(
            url=ApiRoutes.ADD_PRODUCT_TO_CART_PATTERN.path().format(
                product_id=product_id
            ),
            params=params,
        )

    def remove_product_from_cart(self, product_id: int) -> AssertableResponse:
        return self.get(
            url=ApiRoutes.DELETE_PRODUCT_FROM_CART_PATTERN.path().format(
                product_id=product_id
            )
        )
