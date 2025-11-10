import logging

import pytest
from selene import browser

from src.config.config import CFG
from src.model.test_data import TestData
from src.model.user import UserDTO
from src.service.auth_api_service import AuthApiService
from src.service.user_api_service import UserApiService
from src.util.data_generator import DataGenerator
from src.util.test_thread_id_store import ThreadSafeTestThreadsStore
from src.util.user_store import ThreadSafeUserStore

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)

_user_service = UserApiService()


@pytest.fixture()
def create_user(identify_thread_test):

    # Data
    user = DataGenerator().generate_user()

    # Precondition
    user = _user_service.create_user(user)
    ThreadSafeUserStore().add_user(user)
    return user


@pytest.fixture()
def user_tpl(identify_thread_test):

    # Data
    email = DataGenerator().generate_email()
    password = CFG.default_password
    user = (
        DataGenerator.generate_user()
        .with_email(email)
        .with_password(password)
        .with_test_data(TestData.empty().with_password(password))
    )
    ThreadSafeUserStore().add_user(user)

    return user


@pytest.fixture()
def user_credentials(identify_thread_test):

    # Data
    email = DataGenerator().generate_email()
    password = CFG.default_password
    user = (
        UserDTO.empty()
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
