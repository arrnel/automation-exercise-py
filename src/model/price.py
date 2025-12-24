from dataclasses import dataclass
from decimal import Decimal

from src.model.enum.currency import Currency


@dataclass
class Price:
    currency: Currency
    amount: Decimal

    @classmethod
    def from_text(cls, text: str) -> "Price":
        currency_str, amount_str = text.strip().split(". ", 1)
        return cls(currency=Currency(currency_str), amount=Decimal(amount_str))

    def get_price_text(self) -> str:
        """
        Returns price as text. Example "Rs. 1000", "Rs 1000.40"
        """
        return f"{self.currency.value}. {self.get_amount_text()}"

    def get_amount_text(self) -> str:
        """
        Returns price amount as text. Example "1000", "1000.40"
        """
        if self.amount is None:
            raise ValueError("Amount can not be null")

        if self.amount % 1 == 0:
            stripped_amount = self.amount.quantize(Decimal("1."), rounding="ROUND_DOWN")
        else:
            stripped_amount = self.amount

        return str(int(stripped_amount)) if stripped_amount % 1 == 0 else str(stripped_amount)

    def set_amount(self, amount: Decimal):
        self.amount = amount

    def add_amount(self, amount: Decimal):
        if self.amount is None:
            self.amount = Decimal("0.0")
        self.amount += amount

    def subtract_amount(self, amount: Decimal):
        if self.amount is None:
            self.amount = Decimal("0.0")
        self.amount -= amount

    def __repr__(self) -> str:
        return f"PriceDTO(currency={self.currency!r}, amount={self.amount!r})"

    def __str__(self) -> str:
        return self.__repr__()
