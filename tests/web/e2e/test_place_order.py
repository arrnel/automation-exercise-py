import allure
import pytest

from src.util.store.user_store import ThreadSafeUserStore
from src.util.test.data_generator import DataGenerator
from tests.web.base_e2e_test import BaseE2ETest


@pytest.mark.e2e_test
@allure.feature("[E2E] Place Order")
class TestPlaceOrder(BaseE2ETest):

    @pytest.mark.usefixtures("open_login_page")
    @allure.label("owner", "arrnel")
    @allure.title("Purchase products with sign up before checkout")
    def test_place_order_with_sign_up_before_checkout(self):
        # Data
        user = DataGenerator.random_user()
        ThreadSafeUserStore().add_user(user)  # Will remove user after test
        product_items = DataGenerator.random_product_items_info(2, 1)
        product1_title = product_items.products_info[0].title
        product2_title = product_items.products_info[1].title
        comment = DataGenerator.random_comment()
        card = DataGenerator.random_credit_card()

        # Steps
        self.login_page.pre_sign_up_component.sign_up(user.name, user.email)
        self.sign_up_page.sign_up_component.send_user_data(user)
        self.account_created_page.header.go_to_products_page()

        self.products_page.products.get_card_by_title(product1_title).add_to_cart()
        self.payment_page.notification.close()
        self.products_page.products.get_card_by_title(product2_title).add_to_cart()
        self.payment_page.notification.close()

        self.products_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(comment)
        self.checkout_page.place_order()

        self.payment_page.payment_card_component.pay(card)

        # Assertions
        self.order_placed_page.check_page_is_visible()

    @pytest.mark.usefixtures("open_products_page")
    @allure.label("owner", "arrnel")
    @allure.title("Purchase products with sign up while checkout")
    def test_place_order_with_sign_up_while_checkout(self):
        # Data
        user = DataGenerator.random_user()
        ThreadSafeUserStore().add_user(user)  # Will remove user after test
        product_items = DataGenerator.random_product_items_info(2, 1)
        product1_title = product_items.products_info[0].title
        product2_title = product_items.products_info[1].title
        comment = DataGenerator.random_comment()
        card = DataGenerator.random_credit_card()

        # Steps
        self.products_page.products.get_card_by_title(product1_title).add_to_cart()
        self.payment_page.notification.close()
        self.products_page.products.get_card_by_title(product2_title).add_to_cart()
        self.payment_page.notification.close()

        self.products_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()
        self.cart_page.notification.navigate()

        self.login_page.pre_sign_up_component.sign_up(user.name, user.email)
        self.sign_up_page.sign_up_component.send_user_data(user)

        self.account_created_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(comment)
        self.checkout_page.place_order()

        self.payment_page.payment_card_component.pay(card)

        # Assertions
        self.order_placed_page.check_page_is_visible()

    @pytest.mark.usefixtures("create_user", "open_login_page")
    @allure.label("owner", "arrnel")
    @allure.title("Purchase products with login before checkout")
    def test_place_order_with_login_before_checkout(self, create_user):
        # Data
        user = create_user
        product_items = DataGenerator.random_product_items_info(2, 1)
        product1_title = product_items.products_info[0].title
        product2_title = product_items.products_info[1].title
        comment = DataGenerator.random_comment()
        card = DataGenerator.random_credit_card()

        # Steps
        self.login_page.login_component.login(user.email, user.password)
        self.main_page.header.go_to_products_page()

        self.products_page.products.get_card_by_title(product1_title).add_to_cart()
        self.payment_page.notification.close()
        self.products_page.products.get_card_by_title(product2_title).add_to_cart()
        self.payment_page.notification.close()

        self.products_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(comment)
        self.checkout_page.place_order()

        self.payment_page.payment_card_component.pay(card)

        # Assertions
        self.order_placed_page.check_page_is_visible()

    @pytest.mark.usefixtures("create_user", "open_products_page")
    @allure.label("owner", "arrnel")
    @allure.title("Purchase products with login while checkout")
    def test_place_order_with_login_while_checkout(self, create_user):
        # Data
        user = create_user
        product_items = DataGenerator.random_product_items_info(2, 1)
        product1_title = product_items.products_info[0].title
        product2_title = product_items.products_info[1].title
        comment = DataGenerator.random_comment()
        card = DataGenerator.random_credit_card()

        # Steps
        self.products_page.products.get_card_by_title(product1_title).add_to_cart()
        self.payment_page.notification.close()
        self.products_page.products.get_card_by_title(product2_title).add_to_cart()
        self.payment_page.notification.close()

        self.products_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()
        self.cart_page.notification.navigate()

        self.login_page.login_component.login(user.email, user.password)

        self.main_page.header.go_to_cart_page()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.add_comment(comment)
        self.checkout_page.place_order()

        self.payment_page.payment_card_component.pay(card)

        # Assertions
        self.order_placed_page.check_page_is_visible()
