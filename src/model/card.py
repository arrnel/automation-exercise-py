from dataclasses import dataclass, replace


@dataclass
class CardInfo:
    name: str | None
    number: str | None
    cvc: str | None
    expiry_month: str | None
    expiry_year: str | None

    def with_name(self, name: str | None) -> "CardInfo":
        return replace(self, name=name)

    def with_number(self, number: str | None) -> "CardInfo":
        return replace(self, number=number)

    def with_cvc(self, cvc: str | None) -> "CardInfo":
        return replace(self, cvc=cvc)

    def with_expiry_month(self, expiry_month: str | None) -> "CardInfo":
        return replace(self, expiry_month=expiry_month)

    def with_expiry_year(self, expiry_year: str | None) -> "CardInfo":
        return replace(self, expiry_year=expiry_year)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"name={self.name!r},\n"
            f"number={self.number!r},\n"
            f"cvc={self.cvc!r},\n"
            f"expiry_month={self.expiry_month!r},\n"
            f"expiry_year={self.expiry_year!r}\n"
            f")"
        )

    def __str__(self) -> str:
        return self.__repr__()
