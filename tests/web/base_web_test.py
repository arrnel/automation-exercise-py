from abc import ABC

import pytest

from src.service.auth_api_service import AuthApiService
from src.service.brand_api_service import BrandApiService
from src.service.product_api_service import ProductApiService
from src.service.user_api_service import UserApiService
from src.ui.page.auth.login_page import LoginPage
from src.ui.page.auth.signup_page import SignUpPage
from src.ui.page.cart_page import CartPage
from src.ui.page.checkout_page import CheckoutPage
from src.ui.page.contact_us_page import ContactUsPage
from src.ui.page.main_page import MainPage
from src.ui.page.operation_status_page import (
    AccountCreatedPage,
    AccountDeletedPage,
    OrderPlacedPage,
)
from src.ui.page.payment_page import PaymentPage
from src.ui.page.product_page import ProductPage
from src.ui.page.products_page import ProductsPage
from src.util.test.data_generator import DataGenerator


@pytest.mark.web_test
class BaseWebTest(ABC):

    def setup_method(self):

        # -------- SERVICES
        self.auth_api_service = AuthApiService()
        self.product_api_service = ProductApiService()
        self.brand_api_service = BrandApiService()
        self.user_api_service = UserApiService()

        # -------- PAGES
        self.login_page = LoginPage()
        self.sign_up_page = SignUpPage()
        self.main_page = MainPage()
        self.products_page = ProductsPage()
        self.product_page = ProductPage()
        self.cart_page = CartPage()
        self.checkout_page = CheckoutPage()
        self.payment_page = PaymentPage()
        self.order_placed_page = OrderPlacedPage()
        self.account_created_page = AccountCreatedPage()
        self.account_deleted_page = AccountDeletedPage()
        self.contact_us_page = ContactUsPage()

        # -------- UTILS
        self.data_generator = DataGenerator()
