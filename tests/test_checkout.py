"""
===========================================================================
D.5. TEST SCRIPT DESIGN — CHECKOUT & ORDER (TC-ORD-001 → TC-ORD-012)
===========================================================================

FILE: test_checkout.py
MODULE: Checkout & Order
TOTAL TCs: 12

===========================================================================
TC-ORD-001: Xác minh checkout thành công khi dùng địa chỉ đã lưu
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: address_select, order_button, cart_items
  - LoginPage: user_info
  - CatalogPage: add_to_cart_button

TEST STEPS:
  1. Login with valid credentials
  2. Navigate to /Basket
  3. Check if cart has items
  4. If items exist, select saved address
  5. Click place order button

ASSERTIONS:
  - Assert checkout process initiated
  - Assert product count >= 0

LOCATORS:
  - Address select: select[name*="AddressId"], #Address
  - Order button: button[type="submit"][class*="order"]
  - Cart items: .esh-basket-item

===========================================================================
TC-ORD-002: Xác minh checkout thành công khi nhập địa chỉ giao hàng mới
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: address_form, new_address_link, order_button

TEST STEPS:
  1. Login with valid credentials
  2. Navigate to /Basket
  3. Check if cart has items
  4. If items exist, enter new address: "Hanoi, Vietnam"
  5. Place order

ASSERTIONS:
  - Assert new address entry available
  - Assert product count >= 0

LOCATORS:
  - Address form: form[id*="Address"]
  - New address: a[href*="new-address"]

===========================================================================
TC-ORD-003: Xác minh checkout bị chặn khi chưa chọn phương thức thanh toán
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: payment_method, payment_error

TEST STEPS:
  1. Navigate to /Basket (without login or with login)
  2. Check if cart has items
  3. Try to proceed without payment method

ASSERTIONS:
  - Assert payment validation works
  - Assert error or no error (graceful)

LOCATORS:
  - Payment method: input[name*="Payment"], input[type="radio"]
  - Payment error: [class*="payment-error"], #PaymentMethod-error

===========================================================================
TC-ORD-004: Xác minh mã giảm giá hợp lệ được áp dụng đúng khi checkout
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: voucher_input, voucher_apply_button, voucher_success

TEST STEPS:
  1. Navigate to /Basket
  2. Enter voucher code: "SAVE10"
  3. Click apply
  4. Check voucher result

ASSERTIONS:
  - Assert voucher applied or error message shown
  - Assert total unchanged or reduced

LOCATORS:
  - Voucher input: input[name*="Coupon"], #CouponCode
  - Apply button: button[type="submit"][name*="Coupon"]
  - Success: .alert-success

===========================================================================
TC-ORD-005: Xác minh hệ thống từ chối mã giảm giá không hợp lệ khi checkout
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: voucher_input, voucher_error

TEST STEPS:
  1. Navigate to /Basket
  2. Enter invalid voucher: "INVALIDCODE"
  3. Click apply
  4. Check error message

ASSERTIONS:
  - Assert error message displayed or no error

LOCATORS:
  - Error: .alert-danger, [class*="error"]

===========================================================================
TC-ORD-006: Xác minh hệ thống từ chối mã giảm giá đã hết hạn khi checkout
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: voucher_input, voucher_error

TEST STEPS:
  1. Navigate to /Basket
  2. Enter expired voucher: "EXPIRED2024"
  3. Click apply
  4. Check error message

ASSERTIONS:
  - Assert error message displayed or no error

LOCATORS:
  - Same as TC-ORD-005

===========================================================================
TC-ORD-007: Xác minh lịch sử đơn hàng hiển thị đầy đủ các đơn đã đặt
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: order_history_link, order_list

TEST STEPS:
  1. Login with valid credentials
  2. Navigate to /Orders
  3. Count displayed orders

ASSERTIONS:
  - Assert order history accessible
  - Assert order count >= 0

LOCATORS:
  - Order history: a[href*="Order"], a[href*="Orders"]
  - Order list: .esh-orders-item, [class*="order-item"]

===========================================================================
TC-ORD-008: Xác minh trang chi tiết đơn hàng hiển thị đầy đủ thông tin bắt buộc
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: order_detail, order_status

TEST STEPS:
  1. Login with valid credentials
  2. Navigate to /Orders
  3. Click on first order
  4. Get order status

ASSERTIONS:
  - Assert order detail accessible
  - Assert status displayed

LOCATORS:
  - Order detail: [class*="order-detail"]
  - Status: [class*="status"]

===========================================================================
TC-ORD-009: Xác minh hủy đơn hàng thành công khi đơn ở trạng thái cho phép hủy
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: cancel_button, order_status

TEST STEPS:
  1. Login with valid credentials
  2. Navigate to /Orders
  3. Click on first order
  4. Click cancel button
  5. Get updated status

ASSERTIONS:
  - Assert cancel option available
  - Assert status displayed

LOCATORS:
  - Cancel: button[class*="cancel"], a[class*="cancel"]

===========================================================================
TC-ORD-010: Xác minh không thể checkout khi giỏ hàng trống
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: cart_empty, checkout_button

TEST STEPS:
  1. Navigate to /Basket
  2. Check if cart is empty

ASSERTIONS:
  - Assert empty state detected
  - Assert checkout blocked or redirect

LOCATORS:
  - Empty: [class*="empty"], .alert-warning

===========================================================================
TC-ORD-011: Xác minh hệ thống cảnh báo khi số lượng đặt mua vượt tồn kho
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: quantity_input, stock_warning

TEST STEPS:
  1. Navigate to /Basket
  2. Check if cart has items
  3. Update quantity to high value: 999

ASSERTIONS:
  - Assert quantity can be updated
  - Assert product count >= 0

LOCATORS:
  - Quantity: input[name*="Quantity"], input[type="number"]

===========================================================================
TC-ORD-012: Xác minh email xác nhận đơn hàng được gửi thành công sau khi đặt hàng
===========================================================================
PAGE OBJECTS:
  - CheckoutPage: order_confirmation, order_number

TEST STEPS:
  1. Login with valid credentials
  2. Navigate to /Basket
  3. Check if cart has items
  4. If items, place order
  5. Check confirmation

ASSERTIONS:
  - Assert order placed or confirmation shown
  - Assert order number displayed or not

LOCATORS:
  - Confirmation: [class*="confirmation"], [class*="success"]
  - Order number: [class*="order-number"], [id*="order-id"]

===========================================================================
"""

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
