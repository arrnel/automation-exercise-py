import random
from secrets import choice
from typing import List, Callable

from faker import Faker

from src.config.config import CFG

_DOMAINS = ("com", "org", "ru", "en", "io", "me", "info", "tech")
_DOMAINS_WITH_2_LETTERS = ("ru", "me", "io", "jp", "co", "en", "us", "by", "es")
_DOMAIN_NAMES = ("mail", "gmail", "yahoo", "vk", "outlook", "drawbacks", "zoho")
_DEFAULT_DOMAIN_NAME = f"{CFG.email_domain}"
_DEFAULT_EMAIL_SERVICE = f"{_DEFAULT_DOMAIN_NAME}.com"
_FAKE = Faker()


def _random_domain() -> str:
    return choice(_DOMAINS)


def _random_domain_name() -> str:
    return choice(_DOMAIN_NAMES)


class EmailUtil:

    @staticmethod
    def valid_email() -> "_ValidEmail":
        return _ValidEmail()

    @staticmethod
    def invalid_email() -> "_InvalidEmail":
        return _InvalidEmail()


class _ValidEmail:

    @staticmethod
    def random() -> str:
        generators: List[Callable[[], str]] = [
            _ValidEmail.not_exists_email_service,
            _ValidEmail.has_subdomain_name,
            _ValidEmail.username_contains_dot,
            _ValidEmail.username_contains_plus,
            _ValidEmail.username_contains_dash,
            _ValidEmail.username_with_quotes,
            _ValidEmail.numerical_username,
            _ValidEmail.domain_name_contains_dash,
            _ValidEmail.underscore_username,
            _ValidEmail.domain_length_equal_two,
            _ValidEmail.domain_name_length_equal_two,
        ]
        return choice(generators)()

    @staticmethod
    def not_exists_email_service() -> str:
        """Example, `nasty@hotfix.com`"""
        return _FAKE.email()

    @staticmethod
    def has_subdomain_name() -> str:
        """Example, `email@subdomain.example.com`"""
        return (
            f"{_FAKE.first_name()}@"
            f"{_random_domain_name()}."
            f"{_random_domain_name()}."
            f"{_random_domain()}"
        )

    @staticmethod
    def username_contains_dot() -> str:
        """Example, `firstname.lastname@example.com`"""
        username = f"{_FAKE.first_name().lower()}.{_FAKE.user_name()}"
        return f"{username}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def username_contains_plus() -> str:
        """Example, `firstname+lastname@example.com`"""
        username = f"{_FAKE.first_name().lower()}+{_FAKE.user_name()}"
        return f"{username}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def username_contains_dash() -> str:
        """Example, `my-email@domain.com`"""
        username = f"{_FAKE.first_name().lower()}-{_FAKE.user_name()}"
        return f"{username}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def username_with_quotes() -> str:
        """Example, `\"email\"@example.com`"""
        return f'"{_FAKE.user_name()}"@{_DEFAULT_EMAIL_SERVICE}'

    @staticmethod
    def numerical_username() -> str:
        """Example, `452136523456@example.com`"""
        username = _FAKE.random_number(digits=random.randint(5, 20))
        return f"{username}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def domain_name_contains_dash() -> str:
        """Example, `my.main@do-main.com`"""
        return (
            f"{_FAKE.user_name()}@"
            f"{_random_domain_name()}-"
            f"{_random_domain_name()}."
            f"{_random_domain()}"
        )

    @staticmethod
    def underscore_username() -> str:
        """Example, `_______@example.com`"""
        return f"{"_" * random.randint(5, 20)}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def domain_length_equal_two() -> str:
        """Example, `example@domain.ru`"""
        return f"{_FAKE.user_name()}@{_random_domain_name()}.{choice(_DOMAINS_WITH_2_LETTERS)}"

    @staticmethod
    def domain_name_length_equal_two() -> str:
        """Example, `example@co.jp`"""
        domain_name = _FAKE.lexify(text="??").lower()
        return f"{_FAKE.user_name()}@{domain_name}.{_random_domain()}"


class _InvalidEmail:

    @staticmethod
    def random() -> str:
        generators: List[Callable[[], str]] = [
            _InvalidEmail.without_symbols,
            _InvalidEmail.only_special_symbols,
            _InvalidEmail.without_username,
            _InvalidEmail.text_before_email_address,
            _InvalidEmail.without_dog_symbol,
            _InvalidEmail.multiple_dog_symbols,
            _InvalidEmail.first_symbol_is_dot,
            _InvalidEmail.dot_before_dog_symbol,
            _InvalidEmail.two_dot_symbols_in_row,
            _InvalidEmail.hieroglyphs_instead_of_username,
            _InvalidEmail.text_after_email_address,
            _InvalidEmail.without_domain,
            _InvalidEmail.domain_has_one_letter,
            _InvalidEmail.dash_after_dog_symbol,
            _InvalidEmail.invalid_top_level_domain_web,
            _InvalidEmail.mail_server_with_domain_as_ip_and_port,
        ]
        return choice(generators)()

    @staticmethod
    def without_symbols() -> str:
        """Example, `exampleexamplecom`"""
        return f"{_FAKE.first_name()}{_FAKE.first_name()}".lower()

    @staticmethod
    def only_special_symbols() -> str:
        """Example, `%$@#%.com`"""
        special_symbols = ("{", "}", "!", "&", "?", "/", "<", ">", "=", "🜂")
        username = str.join("", random.sample(special_symbols, random.randint(5, 10)))
        domain_name = str.join("", random.sample(special_symbols, random.randint(3, 4)))
        domain = str.join("", random.sample(special_symbols, random.randint(2, 3)))
        return f"{username}@{domain_name}.{domain}"

    @staticmethod
    def without_username() -> str:
        """Example, `@example.com`"""
        return f"@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def text_before_email_address() -> str:
        """Example, `John Doe &lt;email@example.com&gt;`"""
        return f"{_FAKE.word()} {_FAKE.user_name().lower()}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def without_dog_symbol() -> str:
        """Example, `email.example.com`"""
        return f"{_FAKE.user_name().lower()}.{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def multiple_dog_symbols() -> str:
        """Example, `email@example@example.com`"""
        username = f"{_FAKE.first_name()}@{_FAKE.user_name()}"
        return f"{username.lower()}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def first_symbol_is_dot() -> str:
        """Example, `.email@example.com`"""
        username = "." + _FAKE.first_name()
        return f"{username.lower()}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def dot_before_dog_symbol() -> str:
        """Example, `email.@example.com`"""
        username = _FAKE.first_name() + "."
        return f"{username.lower()}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def two_dot_symbols_in_row() -> str:
        """Example, `email..example@example.com`"""
        username = f"{_FAKE.first_name()}..{_FAKE.user_name()}"
        return f"{username.lower()}@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def hieroglyphs_instead_of_username() -> str:
        """Example, `あいうえお@example.com`"""
        return f"あいうえお@{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def text_after_email_address() -> str:
        """Example, `email@example.com (Text)`"""
        username = _FAKE.user_name().lower()
        text = " " + _FAKE.word()
        return f"{username.lower()}@{_DEFAULT_EMAIL_SERVICE}{text.lower()}"

    @staticmethod
    def without_domain() -> str:
        """Example, `email@example`"""
        return f"{_FAKE.user_name().lower()}@{_DEFAULT_DOMAIN_NAME}"

    @staticmethod
    def domain_has_one_letter() -> str:
        """Example, `email@example.r`"""
        domain = _FAKE.lexify("?").lower()
        return f"{_FAKE.user_name().lower()}@{_DEFAULT_DOMAIN_NAME}.{domain}"

    @staticmethod
    def dash_after_dog_symbol() -> str:
        """Example, `email@-example.com`"""
        return f"{_FAKE.user_name().lower()}@-{_DEFAULT_EMAIL_SERVICE}"

    @staticmethod
    def invalid_top_level_domain_web() -> str:
        """Example, `email@example.web`"""
        return f"{_FAKE.user_name().lower()}@{_DEFAULT_DOMAIN_NAME}.web"

    @staticmethod
    def mail_server_with_domain_as_ip_and_port() -> str:
        """Example, `email@123.123.123.123:123`"""
        return f"{_FAKE.user_name().lower()}@{_FAKE.ipv4()}:{_FAKE.port_number()}"
