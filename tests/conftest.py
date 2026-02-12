import os

import allure
import pytest

from src.config.config import CFG
from src.model.enum.github_issue_type import IssueType
from src.service.github_api_service import GithubApiService
from src.service.user_api_service import UserApiService
from src.util import system_util
from src.util.allure.allure_util import AllureUtil
from src.util.decorator.step_logger import step_log
from src.util.store.issue_store import ThreadSafeIssuesStore
from src.util.store.test_thread_id_store import ThreadSafeTestThreadsStore
from src.util.store.user_store import ThreadSafeUserStore
from src.util.test.data_generator import DataGenerator

_GLOBAL = "GLOBAL"


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
@allure.title("All test fixtures")
def all_tests_fixtures():

    ThreadSafeTestThreadsStore().add_current_thread_to_test(_GLOBAL)

    if os.getenv("ENV", "local") in ["local", "docker"]:

        # ---------------------------------------------------------------------
        # CLEAR (REMOVE/CREATE) ALLURE RESULTS DIR
        # ---------------------------------------------------------------------
        with allure.step("Clear allure-results directory"):
            allure_results_dir = system_util.get_allure_results_path()
            system_util.create_folder(allure_results_dir)
            system_util.remove_all_items_from_folder(
                allure_results_dir, by_remove_folder=False
            )

        # ---------------------------------------------------------------------
        # CLEAR (REMOVE/CREATE) ALLURE RESULTS DIR
        # ---------------------------------------------------------------------

        with allure.step("Clear test temp files directory"):
            download_dir = CFG.browser_download_dir
            system_util.create_folder(download_dir)
            system_util.remove_all_items_from_folder(
                download_dir, by_remove_folder=False
            )

    # ---------------------------------------------------------------------
    # ATTACH TEST CONFIGURATION DATA TO ALLURE
    # ---------------------------------------------------------------------
    with step_log.log("Tests configuration data"):
        AllureUtil.attach_config_data()

    yield

    ThreadSafeTestThreadsStore().add_current_thread_to_test(_GLOBAL)

    # ---------------------------------------------------------------------
    # REMOVE USERS AFTER ALL TESTS
    # ---------------------------------------------------------------------
    with step_log.log("Remove users from backend after all tests"):
        ThreadSafeUserStore().remove_all_tests_users()


@pytest.fixture(autouse=True, scope="function")
@allure.title("Each test fixtures")
def each_test_fixtures(request):
    test_name = request.node.name
    ThreadSafeTestThreadsStore().add_current_thread_to_test(test_name)

    yield
    ThreadSafeTestThreadsStore().add_current_thread_to_test(test_name)

    # ---------------------------------------------------------------------
    # REMOVE ALL TEST USERS AFTER TEST
    # ---------------------------------------------------------------------
    with step_log.log("Remove current test users from backend"):
        ThreadSafeUserStore().remove_test_users()

    # ---------------------------------------------------------------------
    # CLEAR TEST THREADS IDENTITIES
    # ---------------------------------------------------------------------
    ThreadSafeTestThreadsStore().clear_test_threads(test_name)


@pytest.fixture()
@allure.title("Create random user by api")
def create_user(request):

    # Data
    user = DataGenerator().random_user()

    # Precondition
    user = UserApiService().create_user(user)
    ThreadSafeUserStore().add_user(user)
    return user
