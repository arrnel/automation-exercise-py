from src.model.base_model import Model


class CardInfo(Model):
    name: str
    number: str
    cvc: str
    expiry_month: str
    expiry_year: str

    def __repr__(self) -> str:
        return (
            f"CardInfo(name={self.name!r}, number={self.number!r}, cvc={self.cvc!r}, "
            f"expiry_month={self.expiry_month!r}, expiry_year={self.expiry_year!r})"
        )

    def __str__(self) -> str:
        return self.__repr__()
