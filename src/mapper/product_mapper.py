from src.model.category import Category
from src.model.dto.product.product_response import ProductResponseDTO
from src.model.enum.currency import Currency
from src.model.price import Price
from src.model.product import Product
from src.model.product_item_info import ProductItemInfo


class ProductMapper:

    @staticmethod
    def to_product(dto: ProductResponseDTO) -> Product:
        return Product(
            id=dto.id,
            title=dto.name,
            category=Category(
                user_type=dto.category.usertype.usertype, title=dto.category.category
            ),
            brand=dto.brand,
            price=Price.from_text(dto.price),
        )

    @staticmethod
    def to_products(dtos: list[ProductResponseDTO]) -> list[Product]:
        return [ProductMapper.to_product(product) for product in dtos]

    @staticmethod
    def to_product_item_info(product: Product, quantity: int):
        return ProductItemInfo(
            id=product.id,
            title=product.title,
            category=product.category,
            price=product.price,
            quantity=quantity,
            total_price=Price(Currency.RS, product.price.amount * quantity),
        )
