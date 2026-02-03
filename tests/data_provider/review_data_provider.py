from faker.proxy import Faker

import src.util.test.range_util as range_util
from src.util.email_util import EmailUtil
from src.util.test.data_generator import DataGenerator

FAKE = Faker()
INVALID_NAME_ERROR_MESSAGE = "Invalid name!"
INVALID_EMAIL_ERROR_MESSAGE = "Invalid email!"
INVALID_MESSAGE_ERROR_MESSAGE = "Invalid message!"


class ReviewDataProviderUI:

    @staticmethod
    def valid_data_provider():
        return [
            # ----- Name
            (
                "'name' length = min",
                DataGenerator.random_review().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val)
                ),
            ),
            (
                "'name' length = min + 1",
                DataGenerator.random_review().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val + 1)
                ),
            ),
            (
                "'name' length = max - 1",
                DataGenerator.random_review().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val - 1)
                ),
            ),
            (
                "'name' length = max",
                DataGenerator.random_review().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val)
                ),
            ),
            # ----- Email
            (
                "'email' has not exists email service",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().not_exists_email_service()
                ),
            ),
            (
                "'email' contains subdomain",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().has_subdomain_name()
                ),
            ),
            (
                "'email' username contains '.'",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().username_contains_dot()
                ),
            ),
            (
                "'email' username contains '+'",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().username_contains_plus()
                ),
            ),
            (
                "'email' username contains '-'",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().username_contains_dash()
                ),
            ),
            (
                "'email' username is numerical",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().numerical_username()
                ),
            ),
            (
                "'email' domain contains '-'",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().domain_name_contains_dash()
                ),
            ),
            (
                "'email' username contains only underscore '-'",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().underscore_username()
                ),
            ),
            (
                "'email' domain length = 2",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().domain_length_equal_two()
                ),
            ),
            (
                "'email' domain name length = 2",
                DataGenerator.random_review().with_email(
                    EmailUtil.valid_email().domain_name_length_equal_two()
                ),
            ),
            # ----- Message
            (
                "'message' length = min",
                DataGenerator.random_review().with_message(
                    DataGenerator.random_text(range_util.review_message_range.min_val)
                ),
            ),
            (
                "'message' length = min + 1",
                DataGenerator.random_review().with_message(
                    DataGenerator.random_text(
                        range_util.review_message_range.min_val + 1
                    )
                ),
            ),
            (
                "'message' length = max - 1",
                DataGenerator.random_review().with_message(
                    DataGenerator.random_text(
                        range_util.review_message_range.max_val - 1
                    )
                ),
            ),
            (
                "'message' length = max",
                DataGenerator.random_review().with_message(
                    DataGenerator.random_text(range_util.review_message_range.max_val)
                ),
            ),
        ]

    @staticmethod
    def invalid_data_provider():
        return [
            # ----- Name
            (
                "'name' is absent",
                DataGenerator.random_user().with_name(None),
                INVALID_NAME_ERROR_MESSAGE,
            ),
            (
                "'name' is empty",
                DataGenerator.random_user().with_name(""),
                INVALID_NAME_ERROR_MESSAGE,
            ),
            (
                "'name' length = min - 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val - 1)
                ),
                INVALID_NAME_ERROR_MESSAGE,
            ),
            (
                "'name' length = max + 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val + 1)
                ),
                INVALID_NAME_ERROR_MESSAGE,
            ),
            # ----- Email
            (
                "'email' is empty",
                DataGenerator.random_user().with_email(""),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' is word",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_symbols()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains only special symbols",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().only_special_symbols()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' not contains username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_username()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains text before username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().text_before_email_address()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' not contains '@' symbol",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_dog_symbol()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains multiple '@' symbols",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().multiple_dog_symbols()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains '.' before dog symbol",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().dot_before_dog_symbol()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains username hieroglyphs instead of username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().hieroglyphs_instead_of_username()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains text after domain",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().text_after_email_address()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' not contains domain",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_domain()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains domain with one letter",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().domain_has_one_letter()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains '-' after '@'",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().dash_after_dog_symbol()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains invalid top level domain web",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().invalid_top_level_domain_web()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            (
                "'email' contains mail server as ip and port",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().mail_server_with_domain_as_ip_and_port()
                ),
                INVALID_EMAIL_ERROR_MESSAGE,
            ),
            # ----- Message
            (
                "'message' length = min",
                DataGenerator.random_review().with_message(
                    DataGenerator.random_text(range_util.review_message_range.min_val)
                ),
                INVALID_MESSAGE_ERROR_MESSAGE,
            ),
            (
                "'message' length = min + 1",
                DataGenerator.random_review().with_message(
                    DataGenerator.random_text(
                        range_util.review_message_range.min_val + 1
                    )
                ),
                INVALID_MESSAGE_ERROR_MESSAGE,
            ),
            (
                "'message' length = max - 1",
                DataGenerator.random_review().with_message(
                    DataGenerator.random_text(
                        range_util.review_message_range.max_val - 1
                    )
                ),
                INVALID_MESSAGE_ERROR_MESSAGE,
            ),
            (
                "'message' length = max",
                DataGenerator.random_review().with_message(
                    DataGenerator.random_text(range_util.review_message_range.max_val)
                ),
                INVALID_MESSAGE_ERROR_MESSAGE,
            ),
        ]
