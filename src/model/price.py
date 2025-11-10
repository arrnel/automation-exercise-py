from decimal import Decimal

from pydantic import Field

from src.model.base_model import Model
from src.model.enum.currency import Currency


class PriceDTO(Model):

    currency: Currency = Field()
    amount: Decimal = Field()

    @classmethod
    def from_text(cls, text: str) -> "PriceDTO":
        currency_str, amount_str = text.strip().split(". ", 1)
        return cls(currency=Currency[currency_str.upper()], amount=Decimal(amount_str))

    def get_price_text(self) -> str:
        return f"{self.currency.value}. {self.get_amount_text()}"

    def get_amount_text(self) -> str:
        if self.amount is None:
            raise ValueError("Amount can not be null")
        stripped_amount = self.amount.quantize(Decimal("1."), rounding="ROUND_DOWN") if self.amount % 1 == 0 else self.amount
        return str(int(stripped_amount)) if stripped_amount % 1 == 0 else str(stripped_amount)

    def __repr__(self) -> str:
        return f"PriceDTO(currency={self.currency!r}, amount={self.amount!r})"

    def __str__(self) -> str:
        return self.__repr__()
