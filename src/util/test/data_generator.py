import copy
import string
from datetime import date, timedelta
from random import randint, choice
from typing import List, Optional

from faker import Faker

from src.config.config import CFG
from src.ex.exception import ProductNotFoundError
from src.model.brand import Brand
from src.model.card import CardInfo
from src.model.contact import ContactInfo
from src.model.enum.user_title import UserTitle
from src.model.enum.user_type import UserType
from src.model.product import Product
from src.model.product_item_info import ProductItemInfo
from src.model.product_items_info import ProductItemsInfo
from src.model.review import ReviewInfo
from src.model.test_data import TestData
from src.model.user import User
from src.service.brand_api_service import BrandApiService
from src.service.product_api_service import ProductApiService
from src.util import system_util, collection_util

_FAKE = Faker()

_COUNTRIES_LIST = [
    "India",
    "United States",
    "Canada",
    "Australia",
    "Israel",
    "New Zealand",
    "Singapore",
]

_RECOMMENDED_PRODUCTS = [
    "Stylish Dress",
    "Winter Top",
    "Summer White Top",
    "Blue Top",
    "Men Tshirt",
]

_USER_TYPES_CATEGORIES = {
    UserType.WOMEN: ["Dress", "Tops", "Saree"],
    UserType.MEN: ["Tshirts", "Jeans"],
    UserType.KIDS: ["Dress", "Tops & Shirts"],
}

_BRANDS = BrandApiService().get_all_brands()

_PRODUCT_SERVICE = ProductApiService()
_PRODUCTS = _PRODUCT_SERVICE.get_all_products()
_EXPECTED_PRODUCT = [
    product for product in _PRODUCTS if product.id == CFG.expected_product_id
][0]
_EXPECTED_PRODUCTS = [
    product for product in _PRODUCTS if product.id in CFG.expected_products_ids
]


class DataGenerator:

    @staticmethod
    def random_sentence(*args):
        """
        Generate sentence with random count

        Args:
            args: Variable length arguments controlling the sentence length:
                * No args → random length in [8, 20]
                * One int → fixed length (must be >= 1)
                * Two ints → random length in range [min_length, max_length]

        Returns:
            str: Random sentence with random count of words.

        Raises:
            RuntimeError: If more than 2 positional arguments are provided.
            ValueError: If min value is negative or equal 0.
        """
        return _FAKE.sentence(
            nb_words=DataGenerator.__random_length(default_min=2, default_max=10, *args)
        )

    @staticmethod
    def random_birth_date():
        now = date.today()
        min_date = now - timedelta(days=365 * 18)
        max_date = now - timedelta(days=365 * 60)
        days_diff = (min_date - max_date).days
        random_days = randint(0, days_diff)
        return max_date + timedelta(days=random_days)

    @staticmethod
    def random_word(*args: int) -> str:
        return _FAKE.lexify(text="?" * DataGenerator.__random_length(2, 10, *args))

    @staticmethod
    def random_number(*args) -> str:
        """
        Generate string number with random digits

        Args:
            args: Variable length arguments controlling the number length:
                * No args → random length in [2, 100]
                * One int → fixed length (must be >= 1)
                * Two ints → random length in range [min_length, max_length]

        Returns:
            str: Number with random digits.

        Raises:
            RuntimeError: If more than 2 positional arguments are provided.
            ValueError: If min value is negative or equal 0.
        """
        return _FAKE.lexify(
            text="?" * DataGenerator.__random_length(2, 10, *args), letters="0123456789"
        )

    @staticmethod
    def random_text(*args: int) -> str:
        """
        Generate text with random characters

        Args:
            args: Variable length arguments controlling the text length:
                * No args → random length in [2, 100]
                * One int → fixed length (must be >= 1)
                * Two ints → random length in range [min_length, max_length]

        Returns:
            str: Text with random characters.

        Raises:
            RuntimeError: If more than 2 positional arguments are provided.
            ValueError: If min value is negative or equal 0.
        """
        length = DataGenerator.__random_length(2, 100, *args)
        return _FAKE.text(length) if length > 5 else DataGenerator.random_word(length)

    @staticmethod
    def random_password(
        *args: int,
        include_uppercase: bool = True,
        include_special: bool = True,
        include_digits: bool = True,
    ):
        """
        Generate password with random symbols

        Args:
            args: Variable length arguments controlling the password length:
                * No args → random length in [8, 20]
                * One int → fixed length (must be >= 1)
                * Two ints → random length in range [min_length, max_length]
            include_uppercase: (bool, optional):
                Include uppercase letters (A-Z). Defaults to True.
            include_digits (bool, optional):
                Include digits (0-9). Defaults to True.
            include_special(bool, optional):
                Include special characters (!@#$ etc.). Defaults to True.

        Returns:
            str: Password with random characters.

        Raises:
            RuntimeError: If more than 2 positional arguments are provided.
            ValueError: If min value is negative or equal 0.
        """
        return _FAKE.password(
            length=DataGenerator.__random_length(8, 20, *args),
            special_chars=include_special,
            digits=include_digits,
            upper_case=include_uppercase,
            lower_case=True,
        )

    @staticmethod
    def __domains():
        return ["me", "io", "com", "net", "org", "gov"]

    @staticmethod
    def random_domain():
        return choice(DataGenerator.__domains())

    @staticmethod
    def random_email():
        domain = DataGenerator.random_domain()
        domain_name = CFG.email_domain
        nickname = _FAKE.user_name()
        separated = choice([True, False])
        digits = "".join(choice(string.digits) for _ in range(randint(1, 4)))
        return f"{nickname}{f".{digits}" if separated else ""}@{domain_name}.{domain}"

    @staticmethod
    def random_full_name():
        return _FAKE.name()

    @staticmethod
    def random_country():
        return choice(_COUNTRIES_LIST)

    @staticmethod
    def random_user() -> User:
        first_name = _FAKE.first_name()
        last_name = _FAKE.last_name()
        password = CFG.default_password
        phone_number = _FAKE.basic_phone_number()
        birth_date = DataGenerator.random_birth_date()

        return User(
            id=None,
            email=DataGenerator.random_email(),
            password=password,
            name=f"{first_name} {last_name}",
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_title=UserTitle.random(),
            birth_day=birth_date.day,
            birth_month=birth_date.month,
            birth_year=birth_date.year,
            company=_FAKE.company(),
            country=DataGenerator.random_country(),
            state=_FAKE.state(),
            city=_FAKE.city(),
            address1=_FAKE.street_address(),
            address2=_FAKE.secondary_address(),
            zip_code=_FAKE.zipcode(),
            test_data=TestData(
                session_id="", csrf="", password=password, phone_number=phone_number
            ),
        )

    @staticmethod
    def random_user_type():
        return UserType.random()

    @staticmethod
    def random_user_type_except(user_type: UserType):
        return UserType.random_except(user_type)

    @staticmethod
    def random_user_type_category(user_type: UserType):
        categories = _USER_TYPES_CATEGORIES.get(user_type, [])
        if not categories:
            raise ValueError(f"No categories for user type: {user_type}")
        return choice(categories)

    @staticmethod
    def random_user_type_and_category() -> [UserType, str]:
        user_type = UserType.random()
        categories = _USER_TYPES_CATEGORIES.get(user_type, [])
        if not categories:
            raise ValueError(f"No categories for user type: {user_type}")
        return user_type, choice(categories)

    @staticmethod
    def random_brand() -> Brand:
        return choice(_BRANDS)

    @staticmethod
    def random_brand_title() -> str:
        return choice(_BRANDS).title

    @staticmethod
    def brands() -> List[Brand]:
        return _BRANDS

    @staticmethod
    def brand_titles() -> List[str]:
        return [brand.title for brand in _BRANDS]

    @staticmethod
    def product(product_title: str) -> Product:
        product = [p for p in _PRODUCTS if p.title == product_title][0]
        if not product:
            raise ProductNotFoundError(f"Not found product by title: {product_title}")
        return product

    @staticmethod
    def random_product():
        return copy.deepcopy(choice(_PRODUCTS))

    @staticmethod
    def random_products(count: Optional[int] = None) -> List[Product]:
        if not count:
            products_count = DataGenerator.random_quantity()
        elif count < 1:
            raise ValueError("Count must be greater than 0")
        else:
            products_count = count
        return collection_util.get_random_unique_values(_PRODUCTS, products_count)

    @staticmethod
    def random_product_items_info(
        count: Optional[int] = None,
        item_quantity: Optional[int] = None,
        item_quantities: Optional[List[int]] = None,
    ) -> ProductItemsInfo:
        random_products = DataGenerator.random_products(count)
        products_item_list = []
        for i in range(count):
            if item_quantity is not None:
                quantity = item_quantity
            elif item_quantities is not None:
                quantity = item_quantities[i]
            else:
                quantity = DataGenerator.random_quantity()
            products_item_list.append(
                ProductItemInfo.from_product(random_products[i], quantity)
            )
        return ProductItemsInfo.from_products_info(products_item_list)

    @staticmethod
    def recommended_product() -> Product:
        recommended_product_title = choice(_RECOMMENDED_PRODUCTS)
        recommended_product = [
            product
            for product in _PRODUCTS
            if product.title == recommended_product_title
        ][0]
        return copy.deepcopy(recommended_product)

    @staticmethod
    def recommended_product_titles() -> List[str]:
        return copy.copy(_RECOMMENDED_PRODUCTS)

    @staticmethod
    def expected_product() -> Product:
        return copy.deepcopy(_EXPECTED_PRODUCT)

    @staticmethod
    def expected_products_items_info() -> ProductItemsInfo:
        products = DataGenerator.expected_products()
        products_list = []
        for product in products:
            products_list.extend([product] * product.id)
        return ProductItemsInfo.from_products(products_list)

    @staticmethod
    def expected_products() -> List[Product]:
        return copy.deepcopy(_EXPECTED_PRODUCTS)

    @staticmethod
    def random_review() -> ReviewInfo:
        return ReviewInfo(
            email=_FAKE.email(),
            name=_FAKE.name(),
            message=_FAKE.paragraph(nb_sentences=randint(1, 10)),
        )

    @staticmethod
    def random_comment() -> str:
        return _FAKE.paragraph(nb_sentences=randint(1, 5))

    @staticmethod
    def random_credit_card() -> CardInfo:
        start_expiry_year = date.today().year + 1
        end_expiry_year = date.today().year + 6
        expiry_date = _FAKE.credit_card_expire(
            start=date.today().replace(year=start_expiry_year),
            end=date.today().replace(year=end_expiry_year),
        ).split("/")
        return CardInfo(
            name=_FAKE.name(),
            number=_FAKE.credit_card_number(),
            cvc=_FAKE.credit_card_security_code(),
            expiry_month=expiry_date[0],
            expiry_year=expiry_date[1],
        )

    @staticmethod
    def expected_credit_card() -> CardInfo:
        return CardInfo(
            name=CFG.expected_credit_card_name,
            number=CFG.expected_credit_card_number,
            cvc=CFG.expected_credit_card_cvc,
            expiry_month=CFG.expected_credit_card_expiry_month,
            expiry_year=CFG.expected_credit_card_expiry_year,
        )

    @staticmethod
    def random_file_path() -> str:
        files = system_util.get_files_in_directory(CFG.path_to_files)
        if not files:
            raise ValueError(f"No files found in directory: {CFG.path_to_files}")
        return choice(files)

    @staticmethod
    def random_contact_info() -> ContactInfo:
        return ContactInfo(
            email=DataGenerator.random_email(),
            name=DataGenerator.random_full_name(),
            subject=_FAKE.sentence(),
            message=_FAKE.paragraph(nb_sentences=randint(4, 10)),
            path_to_file=DataGenerator.random_file_path(),
        )

    @staticmethod
    def random_quantity(min_value: int = 1, max_value=10) -> int:
        return randint(min_value, max_value)

    @staticmethod
    def __random_length(default_min: int, default_max: int, *args: int) -> int:
        """
        Return positive int from args. Using for calculate str length
        Example:
        - With no arguments: random int between default min or default_max values (inclusive).
        - With one argument: first arg.
        - With two arguments: random int between first and second args.

        Raises
        ------
        ValueError
            If more than 2 arguments are provided.
        """
        if len(args) == 0:
            return randint(default_min, default_max)
        elif len(args) == 1:
            if args[0] < 1:
                raise ValueError("Min value must be greater than or equal to 1")
            return args[0]
        elif len(args) == 2:
            min_val, max_val = args[0], args[1]
            if min_val > max_val:
                min_val, max_val = max_val, min_val
            if args[0] < 1:
                raise ValueError("Min value must be greater than or equal to 1")
            return randint(min_val, max_val)
        else:
            raise RuntimeError(
                "Available args count: 0 - random, 1 - fixed, 2 - random in range"
            )
