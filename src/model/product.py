from pydantic import Field, field_validator

from src.model.base_model import Model
from src.model.category import CategoryDTO
from src.model.price import PriceDTO


class ProductDTO(Model):
    id: int = Field(alias="id")
    title: str = Field(alias="name")
    category: CategoryDTO = Field(alias="category")
    brand: str = Field(alias="brand")
    price: PriceDTO = Field(alias="price")
    availability: str = Field(exclude=True, default="In Stock")
    condition: str = Field(exclude=True, default="New")

    @field_validator('price', mode='before')
    @classmethod
    def parse_price(cls, v):
        if isinstance(v, str):
            return PriceDTO.from_text(v)
        if isinstance(v, dict):
            return PriceDTO(**v)
        return v

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
