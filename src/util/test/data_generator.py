import string
from datetime import date, timedelta
from pathlib import Path
from random import randint, choice, shuffle
from typing import List

from faker import Faker

from src.config.config import CFG
from src.ex.exception import ProductNotFoundError
from src.model.card import CardInfo
from src.model.category import Category
from src.model.contact import ContactInfo
from src.model.price import Price
from src.model.product import Product
from src.model.review import ReviewInfo
from src.model.test_data import TestData
from src.model.user import User
from src.model.enum.user_title import UserTitle
from src.model.enum.user_type import UserType
from src.service.product_api_service import ProductApiService

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

_BRANDS = [
    "Polo",
    "H&M",
    "Madame",
    "Mast & Harbour",
    "Babyhug",
    "Allen Solly Junior",
    "Kookie Kids",
    "Biba",
]

_product_service = ProductApiService()

_expected_products_titles = [
    "Sleeveless Dress",
    "Beautiful Peacock Blue Cotton Linen Saree",
    "Pure Cotton V-Neck T-Shirt",
    "Cotton Mull Embroidered Dress",
    "Half Sleeves Top Schiffli Detailing - Pink",
    "Summer White Top",
    "Men Tshirt",
    "Frozen Tops For Kids",
    "Green Side Placket Detail T-Shirt",
    "GRAPHIC DESIGN MEN T SHIRT - BLUE",
]


class DataGenerator:
    __expected_products = None

    @staticmethod
    def random_sentence():
        return _FAKE.sentence()

    @staticmethod
    def random_birth_date():
        now = date.today()
        min_date = now - timedelta(days=365 * 18)
        max_date = now - timedelta(days=365 * 60)
        days_diff = (min_date - max_date).days
        random_days = randint(0, days_diff)
        return max_date + timedelta(days=random_days)

    @staticmethod
    def random_word(a: int, b: int | None = None) -> str:
        return (
            _FAKE.lexify(text="?" * a)
            if b is None
            else _FAKE.lexify(text="?" * randint(a, b))
        )

    @staticmethod
    def random_password(
            min_length: int = 8,
            max_length: int = 20,
            include_uppercase: bool = True,
            include_special: bool = True,
            include_digits: bool = True,
    ):
        return _FAKE.password(
            length=randint(min_length, max_length),
            special_chars=include_special,
            digits=include_digits,
            upper_case=include_uppercase,
            lower_case=True,
        )

    @staticmethod
    def random_email():
        domain = choice(["com", "net", "org", "me", "gov"])
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
    def random_brand() -> str:
        return choice(_BRANDS)

    @staticmethod
    def brands() -> List[str]:
        return _BRANDS

    @staticmethod
    def random_product():
        products = _product_service.get_all_products()
        if not products:
            raise ValueError("No products available")
        return choice(products)

    @staticmethod
    def random_products(count: int) -> List[Product]:
        products = _product_service.get_all_products()
        if count < 1:
            raise ValueError("Count must be greater than 0")
        if len(products) < count:
            raise ValueError(
                f"Invalid products count: {count}. Found products count: {len(products)}"
            )
        shuffle(products)
        return products[:count]

    @staticmethod
    def recommended_product():
        recommended_product_title = choice(_RECOMMENDED_PRODUCTS)
        product = _product_service.get_product_by_title(recommended_product_title)
        if not product:
            raise ProductNotFoundError(
                f"Recommended product not found by title: {recommended_product_title}"
            )
        return product

    @staticmethod
    def expected_product():
        return Product(
            id=3,
            title="Sleeveless Dress",
            category=Category(user_type=UserType.WOMEN, title="Dress"),
            price=Price.from_text("Rs. 1000"),
            brand="Madame",
        )

    @staticmethod
    def get_expected_products_titles() -> List[str]:
        return _expected_products_titles.copy()

    @staticmethod
    def get_expected_products() -> List[Product]:
        if DataGenerator.__expected_products is None:
            DataGenerator.__expected_products = [
                p
                for p in _product_service.get_all_products()
                if p.title in _expected_products_titles
            ]
        return DataGenerator.__expected_products.copy()

    @staticmethod
    def random_review():
        return ReviewInfo(
            email=_FAKE.email(),
            name=_FAKE.name(),
            message=_FAKE.paragraph(nb_sentences=randint(1, 10)),
        )

    @staticmethod
    def generate_comment():
        return _FAKE.paragraph(nb_sentences=randint(1, 5))

    @staticmethod
    def generate_credit_card():
        expiry_date = _FAKE.credit_card_expire().split("/")
        return CardInfo(
            name=_FAKE.name(),
            number=_FAKE.credit_card_number(),
            cvc=_FAKE.credit_card_security_code(),
            expiry_month=expiry_date[0],
            expiry_year=expiry_date[1],
        )

    @staticmethod
    def random_file_path():
        file_names = ["bug.pdf", "file.txt", "img.jpg", "img.png", "img.gif"]
        random_file = Path(CFG.path_to_files()) / choice(file_names)
        return random_file.joinpath().absolute().as_posix()

    @staticmethod
    def random_contact_info():
        return ContactInfo(
            email=DataGenerator.random_email(),
            name=DataGenerator.random_full_name(),
            subject=_FAKE.sentence(),
            message=_FAKE.paragraph(nb_sentences=randint(4, 10)),
            path_to_file=DataGenerator.random_file_path(),
        )
