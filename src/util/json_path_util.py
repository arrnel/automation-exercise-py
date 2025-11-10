from jsonpath_ng.ext import parse

from src.ex.exception import ParseByJsonPathError


# def matches_by_json_path(data: dict, path: str):
#     expr = parse(path)
#     matches = expr.find(data)
#     return [match.value for match in matches]


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

    # BRAND RESPONSE
    BRAND_BRANDS_TITLE = "brands[*].brand"

    # PRODUCT RESPONSE
    PRODUCT_PRODUCTS = "products[*]"
    PRODUCT_PRODUCTS_TITLE = "products[*].name"
    PRODUCT_BRAND_TITLE = "products[*].brand.brand"
