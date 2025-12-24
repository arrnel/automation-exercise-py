from faker.proxy import Faker

import src.util.test.range_util as range_util
from src.util.email_util import EmailUtil
from src.util.test.data_generator import DataGenerator

FAKE = Faker()
USER_NOT_CREATED_MESSAGE = "User not created!"
USER_NOT_UPDATED_MESSAGE = "User not updated!"
MAX_AVAILABLE_YEAR = ""


class UserDataProviderUI:

    @staticmethod
    def valid_sensitive_data_provider():
        return [
            # Name
            (
                "'name' length = min",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val)
                ),
            ),
            (
                "'name' length = min + 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val + 1)
                ),
            ),
            (
                "'name' length = max - 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val - 1)
                ),
            ),
            (
                "'name' length = max",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val)
                ),
            ),
            # first_name
            (
                "'first_name' length = min",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val)
                ),
            ),
            (
                "'first_name' length = min + 1",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val + 1)
                ),
            ),
            (
                "'first_name' length = max - 1",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.max_val - 1)
                ),
            ),
            (
                "'first_name' length = max",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.max_val)
                ),
            ),
            # Last name
            (
                "'last_name' length = min",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val)
                ),
            ),
            (
                "'last_name' length = min + 1",
                DataGenerator.random_user().with_last_name(
                    range_util.first_name_range.min_val + 1
                ),
            ),
            (
                "'last_name' length = max - 1",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.last_name_range.max_val - 1)
                ),
            ),
            (
                "'last_name' length = max",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.last_name_range.max_val)
                ),
            ),
            # Phone number
            (
                "'mobile_number' length = min",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(range_util.phone_number_range.min_val)
                ),
            ),
            (
                "'mobile_number' length = min + 1",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(
                        range_util.phone_number_range.min_val + 1
                    )
                ),
            ),
            (
                "'mobile_number' length = max - 1",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(
                        range_util.phone_number_range.max_val - 1
                    )
                ),
            ),
            (
                "'mobile_number' length = max",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(range_util.phone_number_range.max_val)
                ),
            ),
            # Birth day
            (
                "'birth_day' = 1",
                DataGenerator.random_user().with_birth_day(1),
            ),
            (
                "'birth_day' length = 31",
                DataGenerator.random_user().with_birth_day(31),
            ),
            # Birth month
            (
                "'birth_month' = 1",
                DataGenerator.random_user().with_birth_month(1),
            ),
            (
                "'birth_month' = 12",
                DataGenerator.random_user().with_birth_month(12),
            ),
            # Birth year
            (
                "'birth_year' = 1",
                DataGenerator.random_user().with_birth_month(1),
            ),
            (
                "'birth_year' = 10000",
                DataGenerator.random_user().with_birth_month(12),
            ),
            # Company (Optional)
            (
                "'company' length = min",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.min_val)
                ),
            ),
            (
                "'company' length = min + 1",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.min_val + 1)
                ),
            ),
            (
                "'company' length = max - 1",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.max_val - 1)
                ),
            ),
            (
                "'company' length = max",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.max_val)
                ),
            ),
            # State
            (
                "'state' length = min",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.min_val)
                ),
            ),
            (
                "'state' length = min + 1",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.min_val + 1)
                ),
            ),
            (
                "'state' length = max - 1",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.max_val - 1)
                ),
            ),
            (
                "'state' length = max",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.max_val)
                ),
            ),
            # City
            (
                "'city' length = min",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.min_val)
                ),
            ),
            (
                "'city' length = min + 1",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.min_val + 1)
                ),
            ),
            (
                "'city' length = max - 1",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.max_val - 1)
                ),
            ),
            (
                "'city' length = max",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.max_val)
                ),
            ),
            # Address 1
            (
                "'address1' length = min",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_word(range_util.address1_range.min_val)
                ),
            ),
            (
                "'address1' length = min + 1",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_word(range_util.address1_range.min_val + 1)
                ),
            ),
            (
                "'address1' length = max - 1",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_word(range_util.address1_range.max_val - 1)
                ),
            ),
            (
                "'address1' length = max",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_word(range_util.address1_range.max_val)
                ),
            ),
            # Address 2 (Optional)
            (
                "'address2' length = min",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_word(range_util.address2_range.min_val)
                ),
            ),
            (
                "'address2' length = min + 1",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_word(range_util.address2_range.min_val + 1)
                ),
            ),
            (
                "'address2' length = max - 1",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_word(range_util.address2_range.max_val - 1)
                ),
            ),
            (
                "'address2' length = max",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_word(range_util.address2_range.max_val)
                ),
            ),
            # Zip code
            (
                "'zipcode' length = min",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.min_val)
                ),
            ),
            (
                "'zipcode' length = min + 1",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.min_val + 1)
                ),
            ),
            (
                "'zipcode' length = max - 1",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.max_val - 1)
                ),
            ),
            (
                "'zipcode' length = max",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.max_val)
                ),
            ),
        ]

    @staticmethod
    def invalid_sensitive_data_provider():
        return [
            # Name
            (
                "'name' is empty",
                DataGenerator.random_user().with_name(""),
            ),
            (
                "'name' length = min - 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val - 1)
                ),
            ),
            (
                "'name' length = max + 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val + 1)
                ),
            ),
            # first_name
            (
                "'first_name' is empty",
                DataGenerator.random_user().with_first_name(""),
            ),
            (
                "'first_name' length = min - 1",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val - 1)
                ),
            ),
            (
                "'first_name' length = max + 1",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.max_val + 1)
                ),
            ),
            # Last name
            (
                "'last_name' is empty",
                DataGenerator.random_user().with_last_name(""),
            ),
            (
                "'last_name' length = min - 1",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.last_name_range.min_val - 1)
                ),
            ),
            (
                "'last_name' length = max + 1",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.last_name_range.max_val + 1)
                ),
            ),
            # Email
            (
                "'email' is empty",
                DataGenerator.random_user().with_email(""),
            ),
            (
                "'email' is word",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_symbols()
                ),
            ),
            (
                "'email' contains only special symbols",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().only_special_symbols()
                ),
            ),
            (
                "'email' not contains username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_username()
                ),
            ),
            (
                "'email' contains text before username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().text_before_email_address()
                ),
            ),
            (
                "'email' not contains '@' symbol",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_dog_symbol()
                ),
            ),
            (
                "'email' contains multiple '@' symbols",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().multiple_dog_symbols()
                ),
            ),
            (
                "'email' contains '.' before dog symbol",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().dot_before_dog_symbol()
                ),
            ),
            (
                "'email' contains username hieroglyphs instead of username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().hieroglyphs_instead_of_username()
                ),
            ),
            (
                "'email' contains text after domain",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().text_after_email_address()
                ),
            ),
            (
                "'email' not contains domain",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_domain()
                ),
            ),
            (
                "'email' contains domain with one letter",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().domain_has_one_letter()
                ),
            ),
            (
                "'email' contains '-' after '@'",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().dash_after_dog_symbol()
                ),
            ),
            (
                "'email' contains invalid top level domain web",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().invalid_top_level_domain_web()
                ),
            ),
            (
                "'email' contains mail server as ip and port",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().mail_server_with_domain_as_ip_and_port()
                ),
            ),
            # Phone number
            (
                "'mobile_number' is empty",
                DataGenerator.random_user().with_phone_number(""),
            ),
            (
                "'mobile_number' length = min - 1",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(
                        range_util.phone_number_range.min_val - 1
                    )
                ),
            ),
            (
                "'mobile_number' length = max + 1",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(
                        range_util.phone_number_range.max_val + 1
                    )
                ),
            ),
            (
                "'mobile_number' has invalid format",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(range_util.phone_number_range.min_val)
                ),
            ),
            # Company (Optional)
            (
                "'company' length = min - 1",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.min_val - 1)
                ),
            ),
            (
                "'company' length = max + 1",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.max_val + 1)
                ),
            ),
            # State
            (
                "'state' is empty",
                DataGenerator.random_user().with_state(""),
            ),
            (
                "'state' length = min - 1",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.min_val - 1)
                ),
            ),
            (
                "'state' length = max + 1",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.max_val + 1)
                ),
            ),
            # City
            (
                "'city' is empty",
                DataGenerator.random_user().with_city(""),
            ),
            (
                "'city' length = min - 1",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.min_val - 1)
                ),
            ),
            (
                "'city' length = max + 1",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.max_val + 1)
                ),
            ),
            # Address 1
            (
                "'address1' is empty",
                DataGenerator.random_user().with_address1(""),
            ),
            (
                "'address1' length = min - 1",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_text(range_util.address1_range.min_val - 1)
                ),
            ),
            (
                "'address1' length = max + 1",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_text(range_util.address1_range.max_val + 1)
                ),
            ),
            # Address 2 (Optional)
            (
                "'address2' length = min - 1",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_text(range_util.address2_range.min_val - 1)
                ),
            ),
            (
                "'address2' length = max + 1",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_text(range_util.address2_range.max_val + 1)
                ),
            ),
            # Zip code
            (
                "'zipcode' is empty",
                DataGenerator.random_user().with_zip_code(""),
            ),
            (
                "'zipcode' length = min - 1",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_number(range_util.zip_code_range.min_val - 1)
                ),
            ),
            (
                "'zipcode' length = max + 1",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_number(range_util.zip_code_range.max_val + 1)
                ),
            ),
            (
                "'zipcode' has invalid format",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.min_val)
                ),
            ),
        ]


class UserDataProviderApi:

    @staticmethod
    def valid_sensitive_data_provider():
        return [
            # Name
            (
                "'name' length = min",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val)
                ),
            ),
            (
                "'name' length = min + 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val + 1)
                ),
            ),
            (
                "'name' length = max - 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val - 1)
                ),
            ),
            (
                "'name' length = max",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val)
                ),
            ),
            # first_name
            (
                "'first_name' length = min",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val)
                ),
            ),
            (
                "'first_name' length = min + 1",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val + 1)
                ),
            ),
            (
                "'first_name' length = max - 1",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.max_val - 1)
                ),
            ),
            (
                "'first_name' length = max",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.max_val)
                ),
            ),
            # Last name
            (
                "'last_name' length = min",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val)
                ),
            ),
            (
                "'last_name' length = min + 1",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val + 1)
                ),
            ),
            (
                "'last_name' length = max - 1",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.last_name_range.max_val - 1)
                ),
            ),
            (
                "'last_name' length = max",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.last_name_range.max_val)
                ),
            ),
            # Phone number
            (
                "'mobile_number' length = min",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(range_util.phone_number_range.min_val)
                ),
            ),
            (
                "'mobile_number' length = min + 1",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(
                        range_util.phone_number_range.min_val + 1
                    )
                ),
            ),
            (
                "'mobile_number' length = max - 1",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(
                        range_util.phone_number_range.max_val - 1
                    )
                ),
            ),
            (
                "'mobile_number' length = max",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(range_util.phone_number_range.max_val)
                ),
            ),
            # Birth day
            (
                "'birth_day' = 1",
                DataGenerator.random_user().with_birth_day(1),
            ),
            (
                "'birth_day' length = 31",
                DataGenerator.random_user().with_birth_day(31),
            ),
            # Birth month
            (
                "'birth_month' = 1",
                DataGenerator.random_user().with_birth_month(1),
            ),
            (
                "'birth_month' = 12",
                DataGenerator.random_user().with_birth_month(12),
            ),
            # Birth year
            (
                "'birth_year' = 1",
                DataGenerator.random_user().with_birth_month(1),
            ),
            (
                "'birth_year' = 10000",
                DataGenerator.random_user().with_birth_month(12),
            ),
            # Company (Optional)
            (
                "'company' length = min",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.min_val)
                ),
            ),
            (
                "'company' length = min + 1",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.min_val + 1)
                ),
            ),
            (
                "'company' length = max - 1",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.max_val - 1)
                ),
            ),
            (
                "'company' length = max",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.max_val)
                ),
            ),
            # State
            (
                "'state' length = min",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.min_val)
                ),
            ),
            (
                "'state' length = min + 1",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.min_val + 1)
                ),
            ),
            (
                "'state' length = max - 1",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.max_val - 1)
                ),
            ),
            (
                "'state' length = max",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.max_val)
                ),
            ),
            # City
            (
                "'city' length = min",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.min_val)
                ),
            ),
            (
                "'city' length = min + 1",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.min_val + 1)
                ),
            ),
            (
                "'city' length = max - 1",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.max_val - 1)
                ),
            ),
            (
                "'city' length = max",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.max_val)
                ),
            ),
            # Address 1
            (
                "'address1' length = min",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_word(range_util.address1_range.min_val)
                ),
            ),
            (
                "'address1' length = min + 1",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_word(range_util.address1_range.min_val + 1)
                ),
            ),
            (
                "'address1' length = max - 1",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_word(range_util.address1_range.max_val - 1)
                ),
            ),
            (
                "'address1' length = max",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_word(range_util.address1_range.max_val)
                ),
            ),
            # Address 2 (Optional)
            (
                "'address2' length = min",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_word(range_util.address2_range.min_val)
                ),
            ),
            (
                "'address2' length = min + 1",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_word(range_util.address2_range.min_val + 1)
                ),
            ),
            (
                "'address2' length = max - 1",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_word(range_util.address2_range.max_val - 1)
                ),
            ),
            (
                "'address2' length = max",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_word(range_util.address2_range.max_val)
                ),
            ),
            # Zip code
            (
                "'zipcode' length = min",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.min_val)
                ),
            ),
            (
                "'zipcode' length = min + 1",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.min_val + 1)
                ),
            ),
            (
                "'zipcode' length = max - 1",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.max_val - 1)
                ),
            ),
            (
                "'zipcode' length = max",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.max_val)
                ),
            ),
        ]

    @staticmethod
    def invalid_sensitive_data_provider():
        return [
            # Name
            (
                "'name' is absent",
                DataGenerator.random_user().with_name(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'name' is empty",
                DataGenerator.random_user().with_name(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'name' length = min - 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'name' length = max + 1",
                DataGenerator.random_user().with_name(
                    DataGenerator.random_word(range_util.name_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # first_name
            (
                "'first_name' is absent",
                DataGenerator.random_user().with_first_name(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'first_name' is empty",
                DataGenerator.random_user().with_first_name(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'first_name' length = min - 1",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'first_name' length = max + 1",
                DataGenerator.random_user().with_first_name(
                    DataGenerator.random_word(range_util.first_name_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Last name
            (
                "'last_name' is absent",
                DataGenerator.random_user().with_last_name(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'last_name' is empty",
                DataGenerator.random_user().with_last_name(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'last_name' length = min - 1",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.last_name_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'last_name' length = max + 1",
                DataGenerator.random_user().with_last_name(
                    DataGenerator.random_word(range_util.last_name_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Email
            (
                "'email' is empty",
                DataGenerator.random_user().with_email(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' is word",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_symbols()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains only special symbols",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().only_special_symbols()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' not contains username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_username()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains text before username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().text_before_email_address()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' not contains '@' symbol",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_dog_symbol()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains multiple '@' symbols",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().multiple_dog_symbols()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains '.' before dog symbol",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().dot_before_dog_symbol()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains username hieroglyphs instead of username",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().hieroglyphs_instead_of_username()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains text after domain",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().text_after_email_address()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' not contains domain",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().without_domain()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains domain with one letter",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().domain_has_one_letter()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains '-' after '@'",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().dash_after_dog_symbol()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains invalid top level domain web",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().invalid_top_level_domain_web()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'email' contains mail server as ip and port",
                DataGenerator.random_user().with_email(
                    EmailUtil.invalid_email().mail_server_with_domain_as_ip_and_port()
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Phone number
            (
                "'mobile_number' is absent",
                DataGenerator.random_user().with_phone_number(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'mobile_number' is empty",
                DataGenerator.random_user().with_phone_number(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'mobile_number' length = min - 1",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(range_util.last_name_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'mobile_number' length = max + 1",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_number(
                        range_util.phone_number_range.max_val + 1
                    )
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'mobile_number' has invalid format",
                DataGenerator.random_user().with_phone_number(
                    DataGenerator.random_text(range_util.phone_number_range.min_val)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Birth day
            (
                "'birth_day' is absent",
                DataGenerator.random_user().with_birth_day(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_day' is negative",
                DataGenerator.random_user().with_birth_day(-1),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_day' is zero",
                DataGenerator.random_user().with_birth_day(0),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_day' is invalid positive",
                DataGenerator.random_user().with_birth_day(32),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Birth month
            (
                "'birth_month' is absent",
                DataGenerator.random_user().with_birth_month(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_month' is negative",
                DataGenerator.random_user().with_birth_month(-1),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_month' is zero",
                DataGenerator.random_user().with_birth_month(0),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_month' is invalid positive",
                DataGenerator.random_user().with_birth_month(13),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Birth year
            (
                "'birth_year' is absent",
                DataGenerator.random_user().with_birth_year(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_year' is negative",
                DataGenerator.random_user().with_birth_year(-1),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_year' is zero",
                DataGenerator.random_user().with_birth_year(0),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'birth_year' is invalid positive",
                DataGenerator.random_user().with_birth_year(2026),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Company (Optional)
            (
                "'company' is empty",
                DataGenerator.random_user().with_company(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'company' length = min - 1",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'company' length = max + 1",
                DataGenerator.random_user().with_company(
                    DataGenerator.random_word(range_util.company_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # State
            (
                "'state' is absent",
                DataGenerator.random_user().with_state(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'state' is empty",
                DataGenerator.random_user().with_state(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'state' length = min - 1",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'state' length = max + 1",
                DataGenerator.random_user().with_state(
                    DataGenerator.random_word(range_util.state_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # City
            (
                "'city' is absent",
                DataGenerator.random_user().with_city(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'city' is empty",
                DataGenerator.random_user().with_city(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'city' length = min - 1",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'city' length = max + 1",
                DataGenerator.random_user().with_city(
                    DataGenerator.random_word(range_util.city_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Address 1
            (
                "'address1' is absent",
                DataGenerator.random_user().with_address1(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'address1' is empty",
                DataGenerator.random_user().with_address1(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'address1' length = min - 1",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_text(range_util.address1_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'address1' length = max + 1",
                DataGenerator.random_user().with_address1(
                    DataGenerator.random_text(range_util.address1_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Address 2 (Optional)
            (
                "'address2' is empty",
                DataGenerator.random_user().with_address2(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'address2' length = min - 1",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_text(range_util.address2_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'address2' length = max + 1",
                DataGenerator.random_user().with_address2(
                    DataGenerator.random_text(range_util.address2_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            # Zip code
            (
                "'zipcode' is absent",
                DataGenerator.random_user().with_zip_code(None),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'zipcode' is empty",
                DataGenerator.random_user().with_zip_code(""),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'zipcode' length = min - 1",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_number(range_util.zip_code_range.min_val - 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'zipcode' length = max + 1",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_number(range_util.zip_code_range.max_val + 1)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
            (
                "'zipcode' has invalid format",
                DataGenerator.random_user().with_zip_code(
                    DataGenerator.random_word(range_util.zip_code_range.min_val)
                ),
                USER_NOT_UPDATED_MESSAGE,
            ),
        ]
