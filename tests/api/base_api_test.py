import allure
import pytest
from faker.proxy import Faker

from src.client.auth_api_client import AuthApiClient
from src.client.brand_api_client import BrandApiClient
from src.client.product_api_client import ProductApiClient
from src.client.user_api_client import UserApiClient
from src.client.verify_login_api_client import VerifyLoginApiClient
from src.service.auth_api_service import AuthApiService
from src.service.brand_api_service import BrandApiService
from src.service.product_api_service import ProductApiService
from src.service.user_api_service import UserApiService


@allure.tag("api")
@pytest.mark.api_test
class BaseApiTest:

    def setup_method(self):

        self.auth_api_client = AuthApiClient()
        self.brand_api_client = BrandApiClient()
        self.product_api_client = ProductApiClient()
        self.user_api_client = UserApiClient()
        self.verify_login_api_client = VerifyLoginApiClient()

        self.auth_api_servce = AuthApiService()
        self.brand_api_service = BrandApiService()
        self.product_api_service = ProductApiService()
        self.user_api_service = UserApiService()

        self.faker = Faker()
