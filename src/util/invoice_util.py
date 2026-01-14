import re
from decimal import Decimal
from typing import Tuple

from src.model.enum.currency import Currency
from src.model.price import Price
from src.util.decorator.step_logger import step_log
from src.util.file_util import TxtUtil


class InvoiceUtil:

    @step_log.log(
        "Check invoice contains full name = [{full_name}] and price = [{price}]"
    )
    def check_contains_data(self, full_name: str, price: Price) -> None:
        self.check_contains_full_name(full_name)
        self.check_contains_price(price)

    @step_log.log("Check invoice contains full name: {full_name}")
    def check_contains_full_name(self, full_name: str) -> None:
        if self.__full_name != full_name:
            raise AssertionError(
                f"Invoice actual full name does not match with expected full name. "
                f"Expected: {full_name}, "
                f"Actual: {self.__full_name}"
            )

    @step_log.log("Check invoice contains price: {price}")
    def check_contains_price(self, price: Price) -> None:
        if self.__price != price:
            raise AssertionError(
                f"Invoice actual price does not match with expected price. "
                f"Expected: {self.__price}, "
                f"Actual: {price}"
            )

    @staticmethod
    def parse_full_name_and_price(
        path_to_file: str, currency: Currency = Currency.RS
    ) -> Tuple[str, Price]:
        actual_text = TxtUtil(path_to_file).get_row_text(1)
        pattern = re.compile(
            r"""
            Hi\s*
            (?P<name>.*?)
            ,\s*
            Your\ total\ purchase\ amount\ is\s*
            (?P<price>\d+(?:\.\d+)?)
            \.\s*
            Thank\ you
            """,
            re.VERBOSE,
        )

        match = pattern.search(actual_text)
        if not match:
            raise ValueError(
                f"Actual text does not match pattern. Actual text: {actual_text}"
            )

        name = match.group("name")
        price = Price(
            currency=currency,
            amount=Decimal(match.group("price")),
        )
        return name, price
