from http import HTTPStatus
from typing import List

from src.client.brand_api_client import BrandApiClient
from src.client.core.condition.conditions import Conditions
from src.model.brand import BrandDTO
from src.model.enum.content_type import ContentType
from src.util.step_logger import step_log


class BrandApiService:

    def __init__(self):
        self.product_api_client = BrandApiClient()

    @step_log.log("Get all brands")
    def get_all_brands(self) -> List[BrandDTO]:
        return (
            self.product_api_client.send_get_all_brands_request()
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
                Conditions.content_type(ContentType.JSON),
            )
            .extract()
            .as_list(BrandDTO, "brands")
        )
