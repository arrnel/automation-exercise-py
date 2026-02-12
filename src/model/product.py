from dataclasses import dataclass

from src.model.category import Category
from src.model.price import Price


@dataclass
class Product:

    id: int | None
    title: str | None
    category: Category | None
    brand: str | None
    price: Price | None
    availability: str | None = "In Stock"
    condition: str | None = "New"

    def __repr__(self) -> str:
        return (
            f"ProductDTO("
            f"id={self.id!r}, "
            f"title={self.title!r}, "
            f"category={self.category!r}, "
            f"brand={self.brand!r}, "
            f"price={self.price!r}"
            f")"
        )

    def __str__(self) -> str:
        return self.__repr__()
