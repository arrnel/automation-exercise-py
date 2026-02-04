import logging
import random

import allure
import pytest
from selene import browser

from src.browser.driver_manager import DriverManager
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
from src.util.allure.allure_util import AllureUtil
from src.util.selene import browser_util
from src.util.selene.cookie_util import CookieUtil
from src.util.store.cookie_store import ThreadSafeCookieStore
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore
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

    if CFG.allure_attach_test_artifacts == "none":
        return

    if CFG.allure_attach_test_artifacts == "failed" and report.passed:
        return

    try:
        AllureUtil.attach_screenshot()
        AllureUtil.attach_page_source()

        if CFG.is_remote() and CFG.allure_attach_test_video:
            session_id = browser.driver.session_id
            DriverManager().quit()
            AllureUtil.attach_test_video(test_title=item.name, session_id=session_id)
    except Exception as ex:
        logging.error(f"Unable to make test report. Reason: {ex}")


# -------------------------------
# FIXTURES
# -------------------------------
@pytest.fixture(autouse=True, scope="session")
@allure.title("All UI tests fixture")
def all_ui_tests_fixture(all_tests_fixtures):

    ThreadSafeTestThreadsStore().add_current_thread_to_test("GLOBAL")


@pytest.fixture(autouse=True, scope="function")
@allure.title("Each UI test fixture")
def each_ui_test_fixture(request, each_test_fixtures):

    test_name = request.node.name
    ThreadSafeTestThreadsStore().add_current_thread_to_test(test_name)

    # ---------------------------------------------------------------------
    # Init driver
    # ---------------------------------------------------------------------
    with allure.step("Open browser"):
        DriverManager().init_driver()
        browser.open("/")

        if CFG.browser_name == "firefox":
            browser_util.close_browser_tab(tab_number=1, switch_tab_number=0)
            browser.open("/")

    yield

    ThreadSafeTestThreadsStore().add_current_thread_to_test(test_name)
    if CFG.is_local() and not CFG.browser_hold_driver_on_exit:
        # ---------------------------------------------------------------------
        # Close webdriver
        # ---------------------------------------------------------------------
        browser.driver.quit()



# -------------------------------
# Navigation fixtures
# -------------------------------
@pytest.fixture()
@allure.title("Open Login page")
def open_login_page():
    LoginPage().navigate()


@pytest.fixture()
@allure.title("Open Main page")
def open_main_page():
    MainPage().navigate()


@pytest.fixture()
@allure.title("Open Products page")
def open_products_page():
    ProductsPage().navigate()


@pytest.fixture()
@allure.title("Open Random Product page")
def open_product_page():
    product = DataGenerator.random_product()
    ProductPage().navigate(product.id)
    return product


@pytest.fixture()
@allure.title("Open Expected Product page")
def open_expected_product_page():
    product = DataGenerator.expected_product()
    ProductPage().navigate(product.id)
    return product


@pytest.fixture()
@allure.title("Open Cart page")
def open_cart_page():
    CartPage().navigate()


@pytest.fixture()
@allure.title("Open Checkout page")
def open_checkout_page():
    CheckoutPage().navigate()


@pytest.fixture()
@allure.title("Open Payment page")
def open_payment_page():
    PaymentPage().navigate()


@pytest.fixture()
@allure.title("Open Contact Us page")
def open_contact_us_page():
    ContactUsPage().navigate()


# -------------------------------
# Business logic fixtures
# -------------------------------
@pytest.fixture()
@allure.title("Auth by random user")
def auth_user(create_user):
    yield __auth_by_user_and_add_cookies_to_browser(create_user)


@pytest.fixture()
@allure.title("Auth by expected user")
def auth_expected_user():
    expected_user = (
        UserApiService()
        .get_user_by_email(CFG.default_email)
        .with_password(CFG.default_password)
        .with_test_data(TestData.empty().with_password(CFG.default_password))
    )
    yield __auth_by_user_and_add_cookies_to_browser(expected_user)


def __auth_by_user_and_add_cookies_to_browser(user: User):
    auth_data = AuthApiService().sign_in(user.email, user.test_data.password)
    CookieUtil.add_cookies_to_browser(auth_data)
    browser.driver.refresh()
    test_data = UserMapper.lazy_update_test_data(
        user.test_data,
        TestData.empty()
        .with_csrf(auth_data.get(CFG.csrf_cookie_title, None))
        .with_session_id(auth_data.get(CFG.session_id_cookie_title, None)),
    )
    return user.with_test_data(test_data)


@pytest.fixture()
@allure.title("Add random product to cart")
def add_random_product_to_cart() -> ProductItemsInfo:
    product_items = DataGenerator.random_product_items_info(1)
    CartApiService().add_products_to_cart(product_items)
    cookies = ThreadSafeCookieStore().get_cookies(
        CFG.csrf_cookie_title, CFG.session_id_cookie_title
    )
    CookieUtil.add_cookies_to_browser(cookies)
    browser.driver.refresh()

    return product_items


@pytest.fixture()
@allure.title("Add random products to cart")
def add_random_products_to_cart() -> ProductItemsInfo:
    product_items = DataGenerator.random_product_items_info(random.randint(2, 10))
    CartApiService().add_products_to_cart(product_items)
    cookies = ThreadSafeCookieStore().get_cookies(
        CFG.csrf_cookie_title, CFG.session_id_cookie_title
    )
    CookieUtil.add_cookies_to_browser(cookies)
    browser.driver.refresh()

    return product_items


@pytest.fixture()
@allure.title("Add expected product to cart")
def add_expected_product_to_cart() -> ProductItemsInfo:
    product = DataGenerator.expected_product()
    product_items_info = ProductItemsInfo.empty().from_products([product])
    CartApiService().add_product_to_cart(product.id)
    cookies = ThreadSafeCookieStore().get_cookies(
        CFG.csrf_cookie_title, CFG.session_id_cookie_title
    )
    CookieUtil.add_cookies_to_browser(cookies)
    browser.driver.refresh()

    return product_items_info


@pytest.fixture()
@allure.title("Add expected products to cart")
def add_expected_products_to_cart() -> ProductItemsInfo:
    product_items = DataGenerator.expected_products_items_info()
    CartApiService().add_products_to_cart(product_items)
    cookies = ThreadSafeCookieStore().get_cookies(
        CFG.csrf_cookie_title, CFG.session_id_cookie_title
    )
    CookieUtil.add_cookies_to_browser(cookies)
    browser.driver.refresh()

    return product_items


@pytest.fixture()
@allure.title("Open browser as authorized by expected user")
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
    CookieUtil.add_cookies_to_browser(auth_data)
    MainPage().navigate()

    return user


@pytest.fixture()
@allure.title("Open browser as authorized by random user")
def authorized_browser_open(create_user) -> User:
    # ----- Precondition
    auth_data = AuthApiService().sign_in(create_user.email, create_user.password)
    CookieUtil.add_cookies_to_browser(auth_data)
    MainPage().navigate()

    return create_user
