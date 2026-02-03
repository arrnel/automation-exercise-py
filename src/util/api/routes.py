from enum import Enum


class ApiRoutes(Enum):
    LOGIN = "/login"
    LOGOUT = "/logout"
    PRODUCTS_LIST = "/productsList"
    SEARCH_PRODUCTS = "/searchProduct"
    BRANDS_LIST = "/brandsList"
    VERIFY_LOGIN = "/verifyLogin"
    CREATE_USER_ACCOUNT = "/createAccount"
    GET_USER_ACCOUNT = "/getUserDetailByEmail"
    UPDATE_USER_ACCOUNT = "/updateAccount"
    DELETE_USER_ACCOUNT = "/deleteAccount"
    ADD_PRODUCT_TO_CART_PATTERN = "/add_to_cart/{product_id}"
    DELETE_PRODUCT_FROM_CART_PATTERN = "/delete_cart/{product_id}"

    def path(self):
        return self.value
