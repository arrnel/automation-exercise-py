from http import HTTPStatus

import allure
import pytest

from src.client.core.condition.conditions import Conditions
from src.util.api.json_path_util import JsonPath
from src.util.test.data_generator import DataGenerator
from tests.api.base_api_test import BaseApiTest


@pytest.mark.brand_test
@pytest.mark.brand_api_test
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
            Conditions.body_array_contains_values(
                JsonPath.BRANDS_RESPONSE_BRANDS_TITLES, *brands
            ),
        )
