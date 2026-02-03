from jsonpath_ng.ext import parse

from src.ex.exception import ParseByJsonPathError


def matches_by_json_path(data: dict, path: str):
    try:
        expr = parse(path)
        matches = expr.find(data)
        return [match.value for match in matches]
    except Exception as ex:
        raise ParseByJsonPathError(
            f"Unable to extract value by JSONPath: {path}.\nException: {ex}"
        )


class JsonPath:

    # ----- BRANDS RESPONSE
    BRANDS_RESPONSE_BRANDS = "brands[*]"
    BRANDS_RESPONSE_BRANDS_TITLES = "brands[*].brand"

    # ----- PRODUCTS RESPONSE
    PRODUCTS_RESPONSE_PRODUCTS = "products[*]"
    PRODUCTS_RESPONSE_PRODUCT_TITLES = "products[*].name"
    PRODUCTS_RESPONSE_BRAND_TITLES = "products[*].brand.brand"

    # ----- USERS RESPONSE
    USERS_RESPONSE_USERS = "users[*]"
