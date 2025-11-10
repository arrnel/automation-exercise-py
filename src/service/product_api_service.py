from http import HTTPStatus
from typing import List, Optional

from src.client.core.condition.conditions import Conditions
from src.client.product_api_client import ProductApiClient
from src.model.product import ProductDTO
from src.util.step_logger import step_log


class ProductApiService:

    def __init__(self):
        self.product_api_client = ProductApiClient()

    @step_log.log("Get all products")
    def get_all_products(self) -> List[ProductDTO]:
        return (
            self.product_api_client.send_get_all_products_request()
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
            )
            .extract()
            .as_list(ProductDTO, "products")
        )

    @step_log.log("Search products by query: {query}")
    def search_products(self, query: str) -> List[ProductDTO]:
        return (
            self.product_api_client.send_search_products_by_query_request(query)
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
            )
            .extract()
            .as_list(ProductDTO, "products")
        )

    @step_log.log("Get product by title: {title}")
    def get_product_by_title(self, title) -> Optional[ProductDTO]:
        products = (
            self.product_api_client.send_get_all_products_request()
            .extract()
            .as_list(ProductDTO, "products")
        )
        for product in products:
            if product.title == title:
                return product
        return None
