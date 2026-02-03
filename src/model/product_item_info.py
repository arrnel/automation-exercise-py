from dataclasses import dataclass

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

    @classmethod
    def from_product(cls, product: Product, quantity: int) -> "ProductItemInfo":
        return ProductItemInfo(
            id=product.id,
            title=product.title,
            category=product.category,
            price=product.price,
            quantity=quantity,
            total_price=Price(Currency.RS, product.price.amount * quantity),
        )
