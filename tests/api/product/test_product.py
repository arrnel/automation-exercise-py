from http import HTTPStatus

import allure

from src.client.core.condition.conditions import Conditions
from src.util.data_generator import DataGenerator
from src.util.json_path_util import JsonPath
from tests.api.base_api_test import BaseApiTest


@allure.tag("product")
@allure.epic("Product")
@allure.feature("[API] Get Product")
@allure.title("Test Get Product")
class TestProductApi(BaseApiTest):

    @allure.label("owner", "arrnel")
    @allure.story("Get all products")
    @allure.story(
        "[API] Get products should return 200_OK and contains expected product title"
    )
    def test_get_all_products(self):

        # Data
        expected_title = DataGenerator.expected_product().title

        # Steps
        response = self.product_api_client.send_get_all_products_request()

        # Assertions
        response.check(
            # Conditions.content_type(ContentType.JSON), # Expected: JSON, actual: HTML
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
            Conditions.body_array_contains_values(
                JsonPath.PRODUCT_PRODUCTS_TITLE, expected_title
            ),
        )

    @allure.label("owner", "arrnel")
    @allure.story("Filter products by valid query")
    @allure.title(
        "[API] Get products should return 200_OK and contains expected product title"
    )
    def test_search_products(self):

        # Data
        query = "Top"
        exists_products = [
            "Winter Top",
            "Madame Top For Women",
            "Little Girls Mr. Panda Shirt",
        ]
        not_exists_products = DataGenerator.expected_product().title

        # Steps
        response = self.product_api_client.send_search_products_by_query_request(query)

        # Assertions
        response.check(
            # Conditions.content_type(ContentType.JSON), # Expected: JSON, actual: HTML
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
            Conditions.body_array_contains_values(
                JsonPath.PRODUCT_PRODUCTS_TITLE, *exists_products
            ),
            Conditions.body_array_not_contains_values(
                JsonPath.PRODUCT_PRODUCTS_TITLE, not_exists_products
            ),
        )

    def test_search_products_returns_empty_array(self):

        # Data
        query = self.faker.sentence()

        # Steps
        response = self.product_api_client.send_search_products_by_query_request(query)

        # Assertions
        response.check(
            # Conditions.content_type(ContentType.JSON), # Expected: JSON, actual: HTML
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
            Conditions.body_array_is_empty(JsonPath.PRODUCT_PRODUCTS),
        )
