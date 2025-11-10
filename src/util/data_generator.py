import string
from datetime import date, timedelta
from pathlib import Path
from random import randint, choice, shuffle
from typing import List, overload

from faker import Faker

from src.config.config import CFG
from src.ex.exception import ProductNotFoundError
from src.model.card import CardInfo
from src.model.category import CategoryDTO
from src.model.contact import ContactInfo
from src.model.price import PriceDTO
from src.model.product import ProductDTO
from src.model.review import ReviewInfo
from src.model.test_data import TestData
from src.model.user import UserDTO, UserTitle, UserType
from src.service.product_api_service import ProductApiService

FAKE = Faker()

COUNTRIES_LIST = [
    "India",
    "United States",
    "Canada",
    "Australia",
    "Israel",
    "New Zealand",
    "Singapore",
]

RECOMMENDED_PRODUCTS = [
    "Stylish Dress",
    "Winter Top",
    "Summer White Top",
    "Blue Top",
    "Men Tshirt",
]

USER_TYPES_CATEGORIES = {
    UserType.WOMEN: ["Dress", "Tops", "Saree"],
    UserType.MEN: ["Tshirts", "Jeans"],
    UserType.KIDS: ["Dress", "Tops & Shirts"],
}

BRANDS = [
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
    def random_birth_date():
        now = date.today()
        min_date = now - timedelta(days=365 * 18)
        max_date = now - timedelta(days=365 * 60)
        days_diff = (min_date - max_date).days
        random_days = randint(0, days_diff)
        return max_date + timedelta(days=random_days)

    @overload
    @staticmethod
    def generate_word(length: int) -> str:
        return FAKE.lexify(text="?" * length)

    @overload
    @staticmethod
    def generate_word(min_val: int, max_val: int) -> str:
        count = randint(min_val, max_val)
        return FAKE.lexify(text="?" * count)

    @staticmethod
    def generate_word(a: int, b: int | None = None) -> str:
        return (
            FAKE.lexify(text="?" * a)
            if b is None
            else FAKE.lexify(text="?" * randint(a, b))
        )

    @staticmethod
    def generate_password(
        min_length: int = 8,
        max_length: int = 20,
        include_uppercase: bool = True,
        include_special: bool = True,
        include_digits: bool = True,
    ):
        return FAKE.password(
            length=randint(min_length, max_length),
            special_chars=include_special,
            digits=include_digits,
            upper_case=include_uppercase,
            lower_case=True,
        )

    @staticmethod
    def generate_email():
        domain = choice(["com", "net", "org", "me", "gov"])
        domain_name = CFG.email_domain
        nickname = FAKE.user_name()
        separated = choice([True, False])
        digits = "".join(choice(string.digits) for _ in range(randint(1, 4)))
        return f"{nickname}{f".{digits}" if separated else ""}@{domain_name}.{domain}"

    @staticmethod
    def random_full_name():
        return FAKE.name()

    @staticmethod
    def random_country():
        return choice(COUNTRIES_LIST)

    @staticmethod
    def generate_user() -> UserDTO:
        first_name = FAKE.first_name()
        last_name = FAKE.last_name()
        password = CFG.default_password
        phone_number = FAKE.basic_phone_number()
        birth_date = DataGenerator.random_birth_date()

        return UserDTO(
            id=None,
            email=DataGenerator.generate_email(),
            password=password,
            name=f"{first_name} {last_name}",
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_title=UserTitle.random(),
            birth_day=birth_date.day,
            birth_month=birth_date.month,
            birth_year=birth_date.year,
            company=FAKE.company(),
            country=DataGenerator.random_country(),
            state=FAKE.state(),
            city=FAKE.city(),
            address1=FAKE.street_address(),
            address2=FAKE.secondary_address(),
            zip_code=FAKE.zipcode(),
            test_data=TestData(
                session_id="", csrf="", password=password, phone_number=phone_number
            ),
        )

    @staticmethod
    def random_user_type():
        return UserType.random()

    @staticmethod
    def random_user_type_category(user_type: UserType):
        categories = USER_TYPES_CATEGORIES.get(user_type, [])
        if not categories:
            raise ValueError(f"No categories for user type: {user_type}")
        return choice(categories)

    @staticmethod
    def random_brand() -> str:
        return choice(BRANDS)

    @staticmethod
    def brands() -> List[str]:
        return BRANDS

    @staticmethod
    def random_product():
        products = _product_service.get_all_products()
        if not products:
            raise ValueError("No products available")
        return choice(products)

    @staticmethod
    def random_products(count: int) -> List[ProductDTO]:
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
        recommended_product_title = choice(RECOMMENDED_PRODUCTS)
        product = _product_service.get_product_by_title(recommended_product_title)
        if not product:
            raise ProductNotFoundError(
                f"Recommended product not found by title: {recommended_product_title}"
            )
        return product

    @staticmethod
    def expected_product():
        return ProductDTO(
            id=3,
            name="Sleeveless Dress",
            category=CategoryDTO.of(usertype=UserType.WOMEN, category="Dress"),
            price=PriceDTO.from_text("Rs. 1000"),
            brand="Madame",
        )

    @staticmethod
    def get_expected_products_titles() -> List[str]:
        return _expected_products_titles.copy()

    @staticmethod
    def get_expected_products() -> List[ProductDTO]:
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
            email=FAKE.email(),
            name=FAKE.name(),
            message=FAKE.paragraph(nb_sentences=randint(1, 10)),
        )

    @staticmethod
    def generate_comment():
        return FAKE.paragraph(nb_sentences=randint(1, 5))

    @staticmethod
    def generate_credit_card():
        expiry_date = FAKE.credit_card_expire().split("/")
        return CardInfo(
            name=FAKE.name(),
            number=FAKE.credit_card_number(),
            cvc=FAKE.credit_card_security_code(),
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
            email=DataGenerator.generate_email(),
            name=DataGenerator.random_full_name(),
            subject=FAKE.sentence(),
            message=FAKE.paragraph(nb_sentences=randint(4, 10)),
            path_to_file=DataGenerator.random_file_path(),
        )
