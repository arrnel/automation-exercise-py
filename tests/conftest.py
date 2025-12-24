import shutil
from pathlib import Path

import allure
import pytest
from selene import browser

from src.config.config import CFG
from src.model.enum.github_issue_type import IssueType
from src.service.auth_api_service import AuthApiService
from src.service.github_api_service import GithubApiService
from src.service.user_api_service import UserApiService
from src.util import system_util
from src.util.decorator.step_logger import step_log
from src.util.store.issue_store import ThreadSafeIssuesStore
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore
from src.util.store.user_store import ThreadSafeUserStore
from src.util.test.data_generator import DataGenerator

_GLOBAL = "GLOBAL"
_USER_SERVICE = UserApiService()


# ------------------------------
# HOOKS
# -------------------------------
def pytest_collection_modifyitems(session, config, items):
    issues_to_check: set[int] = set()

    for item in items:
        test_func = getattr(item, "function", None)
        if not test_func:
            continue

        meta = getattr(test_func, "__disabled_by_issue__", None)
        if meta:
            issues_to_check.add(meta["issue_id"])

    if not issues_to_check:
        return

    github_api = GithubApiService()
    store = ThreadSafeIssuesStore()

    with step_log.log("Get github issues statuses"):
        for issue_id in issues_to_check:
            try:
                status = github_api.get_issue_state(issue_id)
            except Exception:
                continue

            store.set_issue_state(issue_id, status)


def pytest_runtest_setup(item):
    test_func = getattr(item, "function", None)
    if not test_func:
        return

    meta = getattr(test_func, "__disabled_by_issue__", None)
    if not meta:
        return

    issue_id = meta["issue_id"]
    reason = meta["reason"]

    store = ThreadSafeIssuesStore()
    status = store.get_issue_state(issue_id)

    if status is None:
        pytest.fail(f"Not found issue by id: {issue_id}")

    if status == IssueType.OPEN:
        pytest.skip(reason)


# ------------------------------
# FIXTURES
# -------------------------------
@pytest.fixture(autouse=True, scope="session")
@allure.title("Before all test preconditions")
def before_all_tests_precondition(global_identify_thread_test):

    # ---------------------------------------------------------------------
    # CLEAR (REMOVE/CREATE) ALLURE RESULTS DIR
    # ---------------------------------------------------------------------
    if CFG.remote_type == "none":
        with allure.step("Clear allure-results directory"):
            allure_results_dir = system_util.get_allure_results_path()
            shutil.rmtree(allure_results_dir, ignore_errors=True)
            Path(allure_results_dir).mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------------------
    # ATTACH TEST CONFIGURATION DATA TO ALLURE
    # ---------------------------------------------------------------------
    with step_log.log("Tests configuration data"):
        from src.config import config

        allure.attach(
            body=config.CONFIGURATION_TEXT,
            name="Configuration data",
            attachment_type=allure.attachment_type.TEXT,
        )


@pytest.fixture(autouse=True, scope="function")
@allure.title("Before each test preconditions")
def before_each_test_precondition(identify_thread_test):
    # ---------------------------------------------------------------------
    # SAVE FUNCTION PRECONDITION THREAD ID TO STORE. NEED TO IDENTIFY USERS BY TEST NAME
    # ---------------------------------------------------------------------
    with step_log.log("Save session thread id to store"):
        ThreadSafeTestThreadsStore().add_current_thread_to_test("GLOBAL")


@pytest.fixture()
def create_user(identify_thread_test):

    # Data
    user = DataGenerator().random_user()

    # Precondition
    user = _USER_SERVICE.create_user(user)
    ThreadSafeUserStore().add_user(user)
    return user


@pytest.fixture()
def auth(email: str, password: str):
    cookies = AuthApiService().sign_in(email, password)
    for key, value in cookies.items():
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


@pytest.fixture(autouse=True, scope="session")
@allure.title("Tear down after each test")
def after_each_test_teardown():

    yield

    # ---------------------------------------------------------------------
    # REMOVE ENDED TEST USERS FROM BACKEND AFTER EACH TESTS
    # ---------------------------------------------------------------------
    with step_log.log("Remove current test users from backend"):
        ThreadSafeUserStore().remove_test_users()


@pytest.fixture(autouse=True, scope="session")
@allure.title("Tear down after all test (after after each test precondition)")
def after_all_tests_teardown(global_identify_thread_test):

    yield

    # ---------------------------------------------------------------------
    # REMOVE ALL TESTS USERS FROM BACKEND AFTER ALL TESTS
    # ---------------------------------------------------------------------
    with step_log.log("Remove users from backend after all tests"):
        ThreadSafeUserStore().remove_all_tests_users()


@pytest.fixture(scope="session")
def global_identify_thread_test(request):
    test_name = ""
    try:
        test_name = request.node.name
    except Exception:
        pass
    ThreadSafeTestThreadsStore().add_current_thread_to_test(test_name)


@pytest.fixture(scope="function")
def identify_thread_test(request):
    test_name = ""
    try:
        test_name = request.node.name
    except Exception:
        pass
    ThreadSafeTestThreadsStore().add_current_thread_to_test(test_name)
