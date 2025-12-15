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
            f"CartProductInfo(title={self.title!r}, category={self.category!r}, price={self.price!r}, "
            f"quantity={self.quantity!r}, total={self.total!r})"
        )

    def __str__(self) -> str:
        return self.__repr__()
