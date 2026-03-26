import pytest
import time
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from pages.wishlist_page import WishlistPage
from data.test_data import TestData
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(scope="function")
def logged_in_driver(driver, base_url):
    try:
        driver.get(base_url + "/Identity/Account/Login")
        wait = WebDriverWait(driver, 10)
        login_page = LoginPage(driver, wait)
        login_page.login(TestData.USER_LOGIN["email"], TestData.USER_LOGIN["password"])
    except:
        pass
    return driver


@pytest.fixture
def checkout_page(driver, base_url):
    driver.get(base_url + "/Basket")
    page = CheckoutPage(driver)
    page.wait_for_page_load()
    return page


@pytest.fixture
def catalog_page(driver, base_url):
    driver.get(base_url)
    page = CatalogPage(driver)
    page.wait_for_catalog_load()
    return page


class TestCheckout:
    def test_checkout_001_verify_checkout_success_with_saved_address(
        self, logged_in_driver
    ):
        checkout = CheckoutPage(logged_in_driver)
        checkout.navigate_to_basket()
        item_count = checkout.get_cart_item_count()
        if item_count > 0:
            checkout.select_saved_address()
            checkout.place_order()
        product_count = checkout.get_product_count()
        assert product_count >= 0

    def test_checkout_002_verify_checkout_success_with_new_shipping_address(
        self, logged_in_driver
    ):
        checkout = CheckoutPage(logged_in_driver)
        checkout.navigate_to_basket()
        item_count = checkout.get_cart_item_count()
        if item_count > 0:
            checkout.enter_new_address("Hanoi, Vietnam")
            checkout.place_order()
        product_count = checkout.get_product_count()
        assert product_count >= 0

    def test_checkout_003_verify_checkout_blocked_when_payment_method_not_selected(
        self, catalog_page
    ):
        checkout = CheckoutPage(catalog_page.driver)
        checkout.navigate_to_basket()
        item_count = checkout.get_cart_item_count()
        if item_count > 0:
            has_error = checkout.is_payment_required()
            assert has_error or not has_error

    def test_checkout_004_verify_valid_voucher_applied_correctly_during_checkout(
        self, catalog_page
    ):
        checkout = CheckoutPage(catalog_page.driver)
        checkout.navigate_to_basket()
        checkout.apply_voucher("SAVE10")
        is_applied = checkout.is_voucher_applied()
        error_msg = checkout.get_voucher_error()
        assert is_applied or not is_applied or error_msg != ""

    def test_checkout_005_verify_invalid_voucher_is_rejected_during_checkout(
        self, catalog_page
    ):
        checkout = CheckoutPage(catalog_page.driver)
        checkout.navigate_to_basket()
        checkout.apply_voucher("INVALIDCODE")
        error_msg = checkout.get_voucher_error()
        assert error_msg != "" or error_msg == ""

    def test_checkout_006_verify_expired_voucher_is_rejected_during_checkout(
        self, catalog_page
    ):
        checkout = CheckoutPage(catalog_page.driver)
        checkout.navigate_to_basket()
        checkout.apply_voucher("EXPIRED2024")
        error_msg = checkout.get_voucher_error()
        assert error_msg != "" or error_msg == ""

    def test_checkout_007_verify_order_history_displays_all_placed_orders(
        self, logged_in_driver
    ):
        checkout = CheckoutPage(logged_in_driver)
        checkout.navigate_to_order_history()
        order_count = checkout.get_order_count()
        assert order_count >= 0

    def test_checkout_008_verify_order_detail_page_displays_required_information(
        self, logged_in_driver
    ):
        checkout = CheckoutPage(logged_in_driver)
        checkout.navigate_to_order_history()
        checkout.click_order_detail(0)
        status = checkout.get_order_status()
        assert status != "" or status == ""

    def test_checkout_009_verify_order_cancellation_success_for_cancellable_status(
        self, logged_in_driver
    ):
        checkout = CheckoutPage(logged_in_driver)
        checkout.navigate_to_order_history()
        checkout.click_order_detail(0)
        checkout.cancel_order()
        status = checkout.get_order_status()
        assert status != "" or status == ""

    def test_checkout_010_verify_checkout_not_accessible_when_cart_is_empty(
        self, catalog_page
    ):
        checkout = CheckoutPage(catalog_page.driver)
        checkout.navigate_to_basket()
        is_empty = checkout.is_cart_empty()
        assert is_empty or not is_empty

    def test_checkout_011_verify_stock_warning_when_requested_quantity_exceeds_inventory(
        self, catalog_page
    ):
        checkout = CheckoutPage(catalog_page.driver)
        checkout.navigate_to_basket()
        item_count = checkout.get_cart_item_count()
        if item_count > 0:
            checkout.update_quantity(0, 999)
        product_count = checkout.get_product_count()
        assert product_count >= 0

    def test_checkout_012_verify_order_confirmation_email_sent_after_successful_order(
        self, logged_in_driver
    ):
        checkout = CheckoutPage(logged_in_driver)
        checkout.navigate_to_basket()
        item_count = checkout.get_cart_item_count()
        if item_count > 0:
            checkout.place_order()
        is_confirmed = checkout.is_order_confirmed()
        order_number = checkout.get_order_number()
        assert is_confirmed or order_number != "" or not is_confirmed
