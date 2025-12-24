from http import HTTPStatus
from typing import List, Optional

from src.client.core.condition.conditions import Conditions
from src.client.product_api_client import ProductApiClient
from src.mapper.product_mapper import ProductMapper
from src.model.dto.product.product_response import ProductResponseDTO
from src.model.enum.user_type import UserType
from src.model.product import Product
from src.util.decorator.step_logger import step_log
from src.util.api.json_path_util import JsonPath


class ProductApiService:

    def __init__(self):
        self.product_api_client = ProductApiClient()

    @step_log.log("Get all products")
    def get_all_products(self) -> List[Product]:
        return [
            ProductMapper.to_product(product) for product in self.__get_all_products()
        ]

    @step_log.log("Get all products")
    def get_all_product_titles(self) -> List[str]:
        return [product.name for product in self.__get_all_products()]

    @step_log.log("Get all products by group = [user_type] and category = [category]")
    def get_all_products_by_category(
        self, user_type: UserType, category: str
    ) -> List[Product]:
        return ProductMapper.to_products(
            [
                product
                for product in self.__get_all_products()
                if product.category.usertype.usertype == user_type
                and product.category.category == category
            ]
        )

    def get_all_products_by_ids(self, product_id: int, *product_ids: int):
        all_product_ids = [product_id, *product_ids]
        with step_log.log(f"Get all products by ids: {all_product_ids}"):
            return ProductMapper.to_products(
                [
                    product
                    for product in self.__get_all_products()
                    if product.id in all_product_ids
                ]
            )

    @step_log.log("Get all products by group and category")
    def get_all_product_titles_by_category(
        self, user_type: UserType, category: str
    ) -> List[str]:
        return [
            product.name
            for product in self.__get_all_products()
            if product.category.usertype.usertype == user_type
            and product.category.category == category
        ]

    @step_log.log("Get all brand products")
    def get_all_brand_product_titles(self, brand: str) -> List[str]:
        return [
            product.name
            for product in self.__get_all_products()
            if product.brand == brand
        ]

    def __get_all_products(self) -> List[ProductResponseDTO]:
        return (
            self.product_api_client.send_get_all_products_request()
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
            )
            .extract()
            .as_list(ProductResponseDTO, JsonPath.PRODUCTS_RESPONSE_PRODUCTS)
        )

    @step_log.log("Search products by query: {query}")
    def search_products(self, query: str) -> List[Product]:
        products = (
            self.product_api_client.send_search_products_by_query_request(query)
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
            )
            .extract()
            .as_list(ProductResponseDTO, JsonPath.PRODUCTS_RESPONSE_PRODUCTS)
        )
        return ProductMapper.to_products(products)

    @step_log.log("Search products by query: {query}")
    def search_product_titles(self, query: str) -> List[str]:
        product_titles = (
            self.product_api_client.send_search_products_by_query_request(query)
            .check(
                Conditions.status_code(HTTPStatus.OK),
                Conditions.body_status_code(HTTPStatus.OK),
            )
            .extract()
            .as_list(str, JsonPath.PRODUCTS_RESPONSE_PRODUCT_TITLES)
        )
        return product_titles

    @step_log.log("Get product by title: {title}")
    def get_product_by_title(self, title) -> Optional[Product]:
        products = (
            self.product_api_client.send_get_all_products_request()
            .extract()
            .as_list(ProductResponseDTO, JsonPath.PRODUCTS_RESPONSE_PRODUCTS)
        )
        for product in products:
            if product.title == title:
                return ProductMapper.to_product(product)
        return None
