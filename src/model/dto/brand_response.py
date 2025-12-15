from pydantic import Field

from src.model.base_model import Model


class BrandDTO(Model):
    id: int = Field(alias="id")
    title: str = Field(alias="brand")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"id={self.id!r}, "
            f"title={self.title!r}"
            f")"
        )

    def __str__(self) -> str:
        return self.__repr__()
