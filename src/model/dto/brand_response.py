from pydantic import Field

from src.model.dto.base_model import Model


class BrandResponseDTO(Model):
    id: int = Field(alias="id")
    brand: str = Field(alias="brand")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"title={self.brand!r}"
            f")"
        )

    def __str__(self) -> str:
        return self.__repr__()
