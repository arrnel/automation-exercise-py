from src.model.base_model import Model
from src.model.price import PriceDTO


class CartProductInfo(Model):
    title: str
    category: str
    price: PriceDTO
    quantity: int
    total: PriceDTO

    def __repr__(self) -> str:
        return (
            f"CartProductInfo(title={self.title!r}, category={self.category!r}, price={self.price!r}, "
            f"quantity={self.quantity!r}, total={self.total!r})"
        )

    def __str__(self) -> str:
        return self.__repr__()
