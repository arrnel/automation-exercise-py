import logging

import pytest
from selene import browser

from src.config.config import CFG
from src.model.test_data import TestData
from src.model.user import User
from src.service.auth_api_service import AuthApiService
from src.service.user_api_service import UserApiService
from src.util.api.test_thread_id_store import ThreadSafeTestThreadsStore
from src.util.api.user_store import ThreadSafeUserStore
from src.util.test.data_generator import DataGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)

_USER_SERVICE = UserApiService()


@pytest.fixture()
def create_user(identify_thread_test):

    # Data
    user = DataGenerator().random_user()

    # Precondition
    user = _USER_SERVICE.create_user(user)
    ThreadSafeUserStore().add_user(user)
    return user


@pytest.fixture()
def user_tpl(identify_thread_test):

    # Data
    email = DataGenerator().random_email()
    password = CFG.default_password
    user = (
        DataGenerator.random_user()
        .with_email(email)
        .with_password(password)
        .with_test_data(TestData.empty().with_password(password))
    )
    ThreadSafeUserStore().add_user(user)

    return user


@pytest.fixture()
def user_credentials(identify_thread_test):

    # Data
    email = DataGenerator().random_email()
    password = CFG.default_password
    user = (
        User.empty()
        .with_email(email)
        .with_password(password)
        .with_test_data(TestData.empty().with_password(password))
    )
    ThreadSafeUserStore().add_user(user)

    return user


@pytest.fixture()
def auth(email: str, password: str):
    cookies = AuthApiService().sign_in(email, password)
    for key, value in cookies:
        browser.driver.add_cookie(
            {
                "name": key,
                "value": str(value),
                "domain": CFG.base_url,
                "path": "/",
                "secure": True,
                "httpOnly": False,
            }
        )
    browser.driver.refresh()


@pytest.fixture(autouse=True, scope="function")
def identify_thread_test(request):
    ThreadSafeTestThreadsStore().add_current_thread_to_test(request.node.name)


@pytest.fixture(scope="session")
def identify_global_thread_test(request):
    test_name = request.node.name if request.node.name else "GLOBAL"
    ThreadSafeTestThreadsStore().add_current_thread_to_test(test_name)


@pytest.fixture(autouse=True, scope="function")
def remove_test_users(identify_thread_test):
    yield
    ThreadSafeUserStore().remove_users()


@pytest.fixture(autouse=True, scope="session")
def remove_all_users_after_tests():
    yield
    ThreadSafeUserStore().remove_all_users()
