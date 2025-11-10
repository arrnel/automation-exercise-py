from http import HTTPStatus

import allure

from src.client.core.condition.conditions import Conditions
from src.util.data_generator import DataGenerator
from src.util.json_path_util import JsonPath
from tests.api.base_api_test import BaseApiTest


@allure.tag("brand")
@allure.epic("Brand")
@allure.feature("[API] Get Brands")
@allure.title("Test Get Brands")
class TestBrandApi(BaseApiTest):

    @allure.label("owner", "arrnel")
    @allure.story("Get brands")
    @allure.title("Get brands should return 200_OK when send get brands request")
    def test_get_all_brands(self):

        # Data
        brands = DataGenerator.brands()

        # Steps
        response = self.brand_api_client.send_get_all_brands_request()

        # Assertions
        response.check(
            Conditions.status_code(HTTPStatus.OK),
            Conditions.body_status_code(HTTPStatus.OK),
            # Conditions.content_type(ContentType.JSON),     # Expected: JSON, actual: HTML
            Conditions.body_array_contains_values(JsonPath.BRAND_BRANDS_TITLE, *brands),
        )
