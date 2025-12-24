from src.model.dto.base_model import Model
from src.model.price import Price


class CartProductInfo(Model):
    title: str
    category: str
    price: Price
    quantity: int
    total: Price

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"title={self.title!r}, "
            f"category={self.category!r}, "
            f"price={self.price!r}, "
            f"quantity={self.quantity!r}, "
            f"total={self.total!r}"
            f")"
        )

    def __str__(self) -> str:
        return self.__repr__()
