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
                "valid: name with multiple spaces",
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
