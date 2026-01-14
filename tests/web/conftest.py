import random

import allure
import pytest
from selene import browser

from src.config.browser_new.driver_manager import DriverManager
from src.config.config import CFG
from src.mapper.user_mapper import UserMapper
from src.model.product_items_info import ProductItemsInfo
from src.model.test_data import TestData
from src.model.user import User
from src.service.auth_api_service import AuthApiService
from src.service.cart_api_service import CartApiService
from src.service.user_api_service import UserApiService
from src.ui.page.auth.login_page import LoginPage
from src.ui.page.cart_page import CartPage
from src.ui.page.checkout_page import CheckoutPage
from src.ui.page.contact_us_page import ContactUsPage
from src.ui.page.main_page import MainPage
from src.ui.page.payment_page import PaymentPage
from src.ui.page.product_page import ProductPage
from src.ui.page.products_page import ProductsPage
from src.util import system_util
from src.util.allure.allure_util import AllureUtil
from src.util.selene.cookie_util import CookieUtil
from src.util.test.data_generator import DataGenerator


# -------------------------------
# HOOKS
# -------------------------------
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    if CFG.allure_append_test_artifact == "none":
        return

    if CFG.allure_append_test_artifact == "failed" and report.passed:
        return

    AllureUtil.attach_screenshot()
    AllureUtil.attach_page_source()

    DriverManager().quit()
    AllureUtil.attach_selenoid_video()


# -------------------------------
# FIXTURES
# -------------------------------
@pytest.fixture(autouse=True, scope="session")
@allure.title("Before all ui test preconditions")
def before_all_tests_precondition(global_identify_thread_test):

    # ---------------------------------------------------------------------
    # CLEAR BROWSER DOWNLOAD DIRECTORY
    # ---------------------------------------------------------------------
    system_util.remove_all_files_from_folder(CFG.browser_download_dir, True)


@pytest.fixture()
def open_login_page():
    LoginPage().navigate()


@pytest.fixture()
def open_main_page():
    MainPage().navigate()


@pytest.fixture()
def open_products_page():
    ProductsPage().navigate()


@pytest.fixture()
def open_product_page():
    product = DataGenerator.random_product()
    ProductPage().navigate(product.id)
    return product


@pytest.fixture()
def open_expected_product_page():
    product = DataGenerator.expected_product()
    ProductPage().navigate(product.id)
    return product


@pytest.fixture()
def open_cart_page():
    CartPage().navigate()


@pytest.fixture()
def open_checkout_page():
    CheckoutPage().navigate()


@pytest.fixture()
def open_payment_page():
    PaymentPage().navigate()


@pytest.fixture()
def open_contact_us_page():
    ContactUsPage().navigate()


@pytest.fixture()
def auth_user(create_user):
    auth_data = AuthApiService().sign_in(create_user.email, create_user.password)
    CookieUtil.add_app_cookies(auth_data)
    browser.driver.refresh()

    test_data = UserMapper.lazy_update_test_data(
        create_user.test_data,
        TestData.empty()
        .with_csrf(auth_data.get(CFG.csrf_cookie_title, None))
        .with_session_id(auth_data.get(CFG.session_id_cookie_title, None)),
    )
    yield create_user.with_test_data(test_data)


@pytest.fixture()
def auth_expected_user():
    auth_data = AuthApiService().sign_in(CFG.default_email, CFG.default_password)
    CookieUtil.add_app_cookies(auth_data)
    browser.driver.refresh()

    user = UserApiService().get_user_by_email(CFG.default_email)
    test_data = TestData(
        csrf=auth_data.get(CFG.csrf_cookie_title, None),
        session_id=auth_data.get(CFG.session_id_cookie_title, None),
        password=CFG.default_password,
        phone_number=None,
    )
    return user.with_test_data(test_data)


@pytest.fixture()
def add_random_product_to_cart() -> ProductItemsInfo:
    product_items = DataGenerator.random_product_items_info(1)
    CartApiService().add_products_to_cart(product_items)
    browser.driver.refresh()

    return product_items


@pytest.fixture()
def add_random_products_to_cart() -> ProductItemsInfo:
    product_items = DataGenerator.random_product_items_info(random.randint(2, 10))
    CartApiService().add_products_to_cart(product_items)
    browser.driver.refresh()

    return product_items


@pytest.fixture()
def add_expected_product_to_cart() -> ProductItemsInfo:
    product = DataGenerator.expected_product()
    product_items_info = ProductItemsInfo.empty().from_products([product])
    CartApiService().add_product_to_cart(product.id)
    browser.driver.refresh()

    return product_items_info


@pytest.fixture()
def add_expected_products_to_cart() -> ProductItemsInfo:
    product_items = DataGenerator.expected_products_items_info()
    CartApiService().add_products_to_cart(product_items)
    browser.driver.refresh()

    return product_items


@pytest.fixture()
def authorized_browser_open_by_expected_user() -> User:
    # ----- Precondition
    auth_data = AuthApiService().sign_in(CFG.default_email, CFG.default_password)
    test_data = TestData(
        csrf=auth_data[CFG.csrf_cookie_title],
        session_id=auth_data[CFG.session_id_cookie_title],
        password=CFG.default_password,
        phone_number=None,
    )
    user = (
        UserApiService()
        .get_user_by_email(CFG.default_email)
        .with_password(CFG.default_password)
        .with_test_data(test_data)
    )
    CookieUtil.add_app_cookies(auth_data)
    MainPage().navigate()

    return user


@pytest.fixture()
def authorized_browser_open(create_user) -> User:
    # ----- Precondition
    auth_data = AuthApiService().sign_in(create_user.email, create_user.password)
    CookieUtil.add_app_cookies(auth_data)
    MainPage().navigate()

    return create_user


@pytest.fixture(autouse=True, scope="function")
def configure_browser():
    DriverManager().init_driver()
    # BrowserManager().init_browser()
    browser.open("/")
    yield
    if CFG.remote_type.lower() == "none" and not CFG.browser_hold_driver_on_exit:
        browser.driver.quit()
