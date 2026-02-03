import allure
import pytest

from tests.web.base_web_test import BaseWebTest


@pytest.mark.e2e_test
@allure.epic("E2E")
class BaseE2ETest(BaseWebTest):
    pass
