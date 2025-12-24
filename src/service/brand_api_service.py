from http import HTTPStatus
from typing import List

from src.client.brand_api_client import BrandApiClient
from src.client.core.condition.conditions import Conditions
from src.mapper.brand_mapper import BrandMapper
from src.model.brand import Brand
from src.model.dto.brand_response import BrandResponseDTO
from src.util.decorator.step_logger import step_log
from src.util.api.json_path_util import JsonPath


class BrandApiService:

    def __init__(self):
        self.product_api_client = BrandApiClient()

    @step_log.log("Get all brands")
    def get_all_brands(self) -> List[Brand]:
        brands_response = (
            self.product_api_client.send_get_all_brands_request()
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
                # Conditions.content_type(ContentType.JSON),
            )
            .extract()
            .as_list(BrandResponseDTO, JsonPath.BRANDS_RESPONSE_BRANDS)
        )
        return [
            BrandMapper.to_brand(brand_response) for brand_response in brands_response
        ]
