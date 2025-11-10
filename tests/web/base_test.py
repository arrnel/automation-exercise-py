from abc import ABC

import allure
import pytest

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
from src.util.data_generator import DataGenerator


@allure.tag("web")
@pytest.mark.web_test
class BaseWebTest(ABC):

    def setup_method(self):
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
        self.data_generator = DataGenerator()
