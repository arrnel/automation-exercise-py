import allure
import pytest

from tests.web.base_web_test import BaseWebTest


@pytest.mark.component_test
@allure.epic("WEB Component")
class BaseWebComponentTest(BaseWebTest):
    pass
