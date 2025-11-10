from enum import Enum

from src.config.config import CFG


class ApiRoutes(Enum):

    LOGIN = "/login"
    LOGOUT = "/logout"
    PRODUCTS_LIST = CFG.base_api_url + "/productsList"
    SEARCH_PRODUCTS = CFG.base_api_url + "/searchProduct"
    BRANDS_LIST = CFG.base_api_url + "/brandsList"
    VERIFY_LOGIN = CFG.base_api_url + "/verifyLogin"
    CREATE_USER_ACCOUNT = CFG.base_api_url + "/createAccount"
    GET_USER_ACCOUNT = CFG.base_api_url + "/getUserDetailByEmail"
    UPDATE_USER_ACCOUNT = CFG.base_api_url + "/updateAccount"
    DELETE_USER_ACCOUNT = CFG.base_api_url + "/deleteAccount"

    def path(self):
        return self.value
