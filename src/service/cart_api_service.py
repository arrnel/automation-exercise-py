from http import HTTPStatus

from src.client.cart_api_client import CartApiClient
from src.client.core.condition.conditions import Conditions
from src.model.product_items_info import ProductItemsInfo
from src.util.decorator.step_logger import step_log


class CartApiService:

    def __init__(self):
        self.cart_api_client = CartApiClient()

    @step_log.log("Add [{quantity}] product(s) by id = [{product_id}] to cart")
    def add_product_to_cart(self, product_id: int, quantity: int = 1) -> None:
        self.cart_api_client.add_product_to_cart(product_id, quantity).check(
            Conditions.status_code(HTTPStatus.OK)
        )

    @step_log.log("Add products to cart")
    def add_products_to_cart(self, product_items_info: ProductItemsInfo) -> None:
        for product in product_items_info.products_info:
            self.add_product_to_cart(product.id, product.quantity)

    @step_log.log("Remove product by id [{product_id}] from cart")
    def remove_product_from_cart(self, product_id: int) -> None:
        self.cart_api_client.remove_product_from_cart(product_id).check(
            Conditions.status_code(HTTPStatus.OK)
        )

    @step_log.log("Remove products from cart")
    def remove_products_from_cart(self, product_id: int, *product_ids: int) -> None:
        all_product_ids = {product_id, *product_ids}
        for product_id in all_product_ids:
            self.remove_product_from_cart(product_id)
