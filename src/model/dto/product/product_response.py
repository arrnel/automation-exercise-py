from pydantic import Field

from src.model.dto.base_model import Model
from src.model.dto.product.product_category_response import CategoryResponseDTO


class ProductResponseDTO(Model):
    id: int | None = Field()
    name: str | None = Field()
    category: CategoryResponseDTO | None = Field()
    brand: str | None = Field()
    price: str | None = Field()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"title={self.title!r}, "
            f"category={self.category!r}, "
            f"brand={self.brand!r}, "
            f"price={self.price!r}"
            f")"
        )

    def __str__(self) -> str:
        return self.__repr__()
