from collections import Counter
from dataclasses import dataclass
from decimal import Decimal
from typing import List, Iterable

from src.model.category import Category
from src.model.enum.currency import Currency
from src.model.price import Price
from src.model.product import Product


@dataclass
class ProductItemInfo:
    id: int | None
    title: str | None
    category: Category | None
    price: Price | None
    quantity: int | None
    total_price: Price | None


@dataclass
class ProductItemsInfo:
    products_info: list[ProductItemInfo]
    total_price: Price | None

    @classmethod
    def empty(cls):
        return cls(products_info=[], total_price=None)

    @classmethod
    def from_products_info(cls, products_info: Iterable[ProductItemInfo]):
        prices_list = [
            product.total_price.amount
            for product in products_info
        ]
        all_products_total_price = Decimal(sum(prices_list))
        return cls(list(products_info), total_price=Price(Currency.RS, all_products_total_price))

    @classmethod
    def from_products(cls, products: Iterable[Product]):

        from src.mapper.product_mapper import ProductMapper

        product_titles = {product.title for product in products}
        products_dict = {product.title: product for product in products}
        counter = Counter(product_titles)
        products_item_info_list = [
            ProductMapper.to_product_item_info(products_dict.get(product_title), counter.get(product_title))
            for product_title in product_titles
        ]

        total_prices_list = [product.price.amount for product in products_item_info_list]
        all_products_total_price = Decimal(sum(total_prices_list))
        return cls(products_item_info_list, Price(Currency.RS, all_products_total_price))

    def add_product_items(self, products_item_list: Iterable[ProductItemInfo]) -> None:
        for new_item in products_item_list:
            existing_item = next(
                (item for item in self.products_info if item.id == new_item.id),
                None
            )

            if existing_item:
                existing_item.quantity += new_item.quantity
                existing_item.total_price.add_amount(new_item.total_price.amount)
            else:
                self.products_info.append(new_item)

            self.total_price.add_amount(new_item.total_price.amount)


    def add_products(self, products: Iterable[Product]) -> None:
        from src.mapper.product_mapper import ProductMapper
        products_items_info = [ProductMapper.to_product_item_info(product, 1) for product in products]
        self.add_product_items(products_items_info)

    def remove_by_ids(self, product_id: int, *product_ids: int) -> None:
        all_product_ids = {product_id, *product_ids}

        for product_id in all_product_ids:
            product = next(
                (item for item in self.products_info if item.id == product_id),
                None
            )

            if not product:
                continue

            self.total_price.subtract_amount(product.total_price.amount)
            self.products_info.remove(product)

    def remove_by_titles(self, product_title: str, *product_titles: str) -> None:

        all_product_titles = {product_title, *product_titles}

        for product_title in all_product_titles:
            product = next(
                (item for item in self.products_info if item.title == product_title),
                None
            )

            if not product:
                continue

            self.total_price.subtract_amount(product.total_price.amount)
            self.products_info.remove(product)

    def update_product_quantity_by_id(self, product_id: int, quantity: int) -> None:

        product = next(
            (item for item in self.products_info if item.id == product_id),
            None
        )

        if not product:
            raise ValueError(f"Product with id {product_id} not found")

        delta = product.price.amount * product.quantity-quantity
        product.total_price.add_amount(delta)
        self.total_price.add_amount(delta)
        product.quantity = quantity

    def update_product_quantity_by_title(self, product_title: str, quantity: int) -> None:

        product = next(
            (item for item in self.products_info if item.title == product_title),
            None
        )

        if not product:
            raise ValueError(f"Product with title {product_title} not found")

        delta = product.price.amount * product.quantity - quantity
        product.total_price.add_amount(delta)
        self.total_price.add_amount(delta)
        product.quantity = quantity
