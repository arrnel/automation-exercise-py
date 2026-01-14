from src.util.test import range_util
from src.util.test.data_generator import DataGenerator


class CardDataProviderUI:

    @staticmethod
    def valid_cards():
        return [
            # ===== NAME VALID =====
            (
                "valid: name min length",
                DataGenerator.random_credit_card().with_name("A"),
            ),
            (
                "valid: name max length",
                DataGenerator.random_credit_card().with_name("A" * 50),
            ),
            (
                "valid: common latin name",
                DataGenerator.random_credit_card().with_name("John Doe"),
            ),
            (
                "valid name contains multiple spaces",
                DataGenerator.random_credit_card().with_name("Anna Maria Smith"),
            ),
            # ===== NUMBER VALID =====
            (
                "valid: 16 digits number",
                DataGenerator.random_credit_card().with_number("4242424242424242"),
            ),
            (
                "valid: boundary valid number",
                DataGenerator.random_credit_card().with_number("4000000000000002"),
            ),
            # ===== CVC VALID =====
            ("valid: cvc typical", DataGenerator.random_credit_card().with_cvc("123")),
            # ===== EXPIRY MONTH VALID =====
            (
                "valid: expiry month min",
                DataGenerator.random_credit_card().with_expiry_month("01"),
            ),
            (
                "valid: expiry month max",
                DataGenerator.random_credit_card().with_expiry_month("12"),
            ),
            # ===== EXPIRY YEAR VALID =====
            (
                "valid: future year",
                DataGenerator.random_credit_card().with_expiry_year("30"),
            ),
        ]

    @staticmethod
    def invalid_cards():
        return [
            # ===== NAME =====
            (
                "name is empty",
                DataGenerator.random_credit_card().with_name(""),
            ),
            (
                "name only spaces",
                DataGenerator.random_credit_card().with_name(" " * 5),
            ),
            (
                "name length = min - 1",
                DataGenerator.random_credit_card().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val - 1)
                ),
            ),
            (
                "name length = max + 1",
                DataGenerator.random_credit_card().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val + 1)
                ),
            ),
            (
                "name contains digits",
                DataGenerator.random_credit_card().with_name("JOHN123 DOE"),
            ),
            (
                "name contains special characters",
                DataGenerator.random_credit_card().with_name("JOHN@DOE!"),
            ),
            (
                "name contains emoji",
                DataGenerator.random_credit_card().with_name("JOHN 😀 DOE"),
            ),
            (
                "name contains non latin characters",
                DataGenerator.random_credit_card().with_name("ИВАН ИВАНОВ"),
            ),
            (
                "name contains leading spaces",
                DataGenerator.random_credit_card().with_name("  JOHN DOE"),
            ),
            (
                "name contains trailing spaces",
                DataGenerator.random_credit_card().with_name("JOHN DOE  "),
            ),
            (
                "name contains newline",
                DataGenerator.random_credit_card().with_name("JOHN\nDOE"),
            ),
            # ===== CARD NUMBER =====
            (
                "card number is empty",
                DataGenerator.random_credit_card().with_number(""),
            ),
            (
                "card number only spaces",
                DataGenerator.random_credit_card().with_number(" " * 10),
            ),
            (
                "card number too short",
                DataGenerator.random_credit_card().with_number("411111111111"),
            ),
            (
                "card number too long",
                DataGenerator.random_credit_card().with_number("41111111111111111111"),
            ),
            (
                "card number contains letters",
                DataGenerator.random_credit_card().with_number("4111AAAA1111BBBB"),
            ),
            (
                "card number contains special characters",
                DataGenerator.random_credit_card().with_number("4111!111@111#111"),
            ),
            (
                "card number contains spaces",
                DataGenerator.random_credit_card().with_number("4111 1111 1111 1111"),
            ),
            (
                "card number contains dashes",
                DataGenerator.random_credit_card().with_number("4111-1111-1111-1111"),
            ),
            (
                "card number fails luhn check",
                DataGenerator.random_credit_card().with_number("4111111111111121"),
            ),
            (
                "card number all zeros",
                DataGenerator.random_credit_card().with_number("0000000000000000"),
            ),
            # ===== CVC =====
            (
                "cvc is empty",
                DataGenerator.random_credit_card().with_cvc(""),
            ),
            (
                "cvc only spaces",
                DataGenerator.random_credit_card().with_cvc("   "),
            ),
            (
                "cvc too short",
                DataGenerator.random_credit_card().with_cvc("1"),
            ),
            (
                "cvc too long",
                DataGenerator.random_credit_card().with_cvc("12345"),
            ),
            (
                "cvc contains letters",
                DataGenerator.random_credit_card().with_cvc("12A"),
            ),
            (
                "cvc contains special characters",
                DataGenerator.random_credit_card().with_cvc("!@#"),
            ),
            (
                "cvc all zeros",
                DataGenerator.random_credit_card().with_cvc("000"),
            ),
            # ===== EXPIRY MONTH =====
            (
                "expiry month is empty",
                DataGenerator.random_credit_card().with_expiry_month(""),
            ),
            (
                "expiry month only spaces",
                DataGenerator.random_credit_card().with_expiry_month("  "),
            ),
            (
                "expiry month = 00",
                DataGenerator.random_credit_card().with_expiry_month("00"),
            ),
            (
                "expiry month = 13",
                DataGenerator.random_credit_card().with_expiry_month("13"),
            ),
            (
                "expiry month contains letters",
                DataGenerator.random_credit_card().with_expiry_month("AB"),
            ),
            (
                "expiry month one digit",
                DataGenerator.random_credit_card().with_expiry_month("3"),
            ),
            # ===== EXPIRY YEAR =====
            (
                "expiry year is empty",
                DataGenerator.random_credit_card().with_expiry_year(""),
            ),
            (
                "expiry year only spaces",
                DataGenerator.random_credit_card().with_expiry_year("  "),
            ),
            (
                "expiry year in the past",
                DataGenerator.random_credit_card().with_expiry_year("19"),
            ),
            (
                "expiry year too short",
                DataGenerator.random_credit_card().with_expiry_year("2"),
            ),
            (
                "expiry year too long",
                DataGenerator.random_credit_card().with_expiry_year("203456"),
            ),
            (
                "expiry year contains letters",
                DataGenerator.random_credit_card().with_expiry_year("20AA"),
            ),
        ]
