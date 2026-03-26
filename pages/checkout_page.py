from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    CHECKOUT_LINK = (
        By.CSS_SELECTOR,
        "a[href*='Checkout'], a[href*='checkout'], a[href*='Order']",
    )
    BASKET_LINK = (By.CSS_SELECTOR, "a[href*='Basket'], a[href*='basket']")

    CART_ITEMS = (By.CLASS_NAME, "esh-basket-item")
    CART_ITEM = (By.CSS_SELECTOR, ".esh-basket-item")
    CART_EMPTY = (By.CSS_SELECTOR, "[class*='empty'], .alert-warning")

    QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name*='Quantity'], input[type='number']")
    REMOVE_BTN = (By.CSS_SELECTOR, "[class*='remove'], button[title*='Remove']")

    VOUCHER_INPUT = (
        By.CSS_SELECTOR,
        "input[name*='Coupon'], input[name*='Voucher'], input[id*='Coupon']",
    )
    VOUCHER_APPLY_BTN = (
        By.CSS_SELECTOR,
        "button[type='submit'][name*='Coupon'], button[class*='apply']",
    )
    VOUCHER_ERROR = (
        By.CSS_SELECTOR,
        ".alert-danger, [class*='error'], .field-validation-error",
    )
    VOUCHER_SUCCESS = (By.CSS_SELECTOR, ".alert-success, [class*='success']")

    TOTAL_PRICE = (By.CSS_SELECTOR, "[class*='total'], [class*='Total'], #total-price")
    SUBTOTAL = (By.CSS_SELECTOR, "[class*='subtotal'], .ESH-basket-total")

    CHECKOUT_BUTTON = (
        By.CSS_SELECTOR,
        "button[type='submit'][class*='checkout'], a[class*='checkout']",
    )

    ADDRESS_FORM = (By.CSS_SELECTOR, "form[id*='Address'], [name*='Address']")
    ADDRESS_SELECT = (
        By.CSS_SELECTOR,
        "select[name*='AddressId'], select[id*='Address']",
    )
    NEW_ADDRESS_LINK = (
        By.CSS_SELECTOR,
        "a[href*='new-address'], [class*='new-address']",
    )

    PAYMENT_METHOD = (
        By.CSS_SELECTOR,
        "input[name*='Payment'], input[type='radio'][name*='Payment']",
    )
    PAYMENT_ERROR = (By.CSS_SELECTOR, "[class*='payment-error'], #PaymentMethod-error")

    ORDER_BUTTON = (
        By.CSS_SELECTOR,
        "button[type='submit'][class*='order'], button[class*='place-order']",
    )
    ORDER_CONFIRMATION = (
        By.CSS_SELECTOR,
        "[class*='confirmation'], [class*='success'], [id*='confirmation']",
    )
    ORDER_NUMBER = (By.CSS_SELECTOR, "[class*='order-number'], [id*='order-id']")

    ORDER_HISTORY_LINK = (
        By.CSS_SELECTOR,
        "a[href*='Order'], a[href*='order'], a[href*='Orders']",
    )
    ORDER_LIST = (By.CSS_SELECTOR, ".esh-orders-item, [class*='order-item']")
    ORDER_DETAIL = (By.CSS_SELECTOR, "[class*='order-detail']")
    ORDER_STATUS = (By.CSS_SELECTOR, "[class*='status']")
    CANCEL_ORDER_BTN = (By.CSS_SELECTOR, "button[class*='cancel'], a[class*='cancel']")

    def wait_for_page_load(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.CART_ITEMS)
            )
        except:
            pass

    def navigate_to_basket(self):
        try:
            basket_link = self.driver.find_elements(*self.BASKET_LINK)
            if basket_link:
                basket_link[0].click()
                self.wait_for_page_load()
        except:
            self.driver.get(self.driver.current_url + "/Basket")

    def get_cart_item_count(self):
        try:
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(items)
        except:
            return 0

    def is_cart_empty(self):
        try:
            empty_msg = self.driver.find_elements(*self.CART_EMPTY)
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(empty_msg) > 0 or len(items) == 0
        except:
            return True

    def update_quantity(self, item_index, quantity):
        try:
            items = self.driver.find_elements(*self.CART_ITEM)
            if items and item_index < len(items):
                item = items[item_index]
                qty_input = item.find_elements(*self.QUANTITY_INPUT)
                if qty_input:
                    qty_input[0].clear()
                    qty_input[0].send_keys(str(quantity))
        except:
            pass

    def remove_item(self, item_index=0):
        try:
            items = self.driver.find_elements(*self.CART_ITEM)
            if items and item_index < len(items):
                item = items[item_index]
                remove_btn = item.find_elements(*self.REMOVE_BTN)
                if remove_btn:
                    remove_btn[0].click()
        except:
            pass

    def apply_voucher(self, code):
        try:
            voucher_input = self.driver.find_elements(*self.VOUCHER_INPUT)
            if voucher_input:
                voucher_input[0].clear()
                voucher_input[0].send_keys(code)
                apply_btn = self.driver.find_elements(*self.VOUCHER_APPLY_BTN)
                if apply_btn:
                    apply_btn[0].click()
        except:
            pass

    def get_voucher_error(self):
        try:
            error = self.driver.find_elements(*self.VOUCHER_ERROR)
            return error[0].text if error else ""
        except:
            return ""

    def is_voucher_applied(self):
        try:
            success = self.driver.find_elements(*self.VOUCHER_SUCCESS)
            return len(success) > 0
        except:
            return False

    def get_total_price(self):
        try:
            total = self.driver.find_elements(*self.TOTAL_PRICE)
            return total[0].text if total else ""
        except:
            return ""

    def get_subtotal(self):
        try:
            subtotal = self.driver.find_elements(*self.SUBTOTAL)
            return subtotal[0].text if subtotal else ""
        except:
            return ""

    def select_saved_address(self):
        try:
            address_select = self.driver.find_elements(*self.ADDRESS_SELECT)
            if address_select:
                select = Select(address_select[0])
                select.select_by_index(0)
        except:
            pass

    def enter_new_address(self, address):
        try:
            address_form = self.driver.find_elements(*self.ADDRESS_FORM)
            if address_form:
                pass
        except:
            pass

    def select_payment_method(self, method_index=0):
        try:
            payment_options = self.driver.find_elements(*self.PAYMENT_METHOD)
            if payment_options and method_index < len(payment_options):
                payment_options[method_index].click()
        except:
            pass

    def is_payment_required(self):
        try:
            payment_error = self.driver.find_elements(*self.PAYMENT_ERROR)
            return len(payment_error) > 0
        except:
            return False

    def place_order(self):
        try:
            order_btn = self.driver.find_elements(*self.ORDER_BUTTON)
            if order_btn:
                order_btn[0].click()
        except:
            pass

    def get_order_number(self):
        try:
            order_num = self.driver.find_elements(*self.ORDER_NUMBER)
            return order_num[0].text if order_num else ""
        except:
            return ""

    def is_order_confirmed(self):
        try:
            confirmation = self.driver.find_elements(*self.ORDER_CONFIRMATION)
            return len(confirmation) > 0
        except:
            return False

    def navigate_to_order_history(self):
        try:
            order_link = self.driver.find_elements(*self.ORDER_HISTORY_LINK)
            if order_link:
                order_link[0].click()
        except:
            self.driver.get(self.driver.current_url + "/Orders")

    def get_order_count(self):
        try:
            orders = self.driver.find_elements(*self.ORDER_LIST)
            return len(orders)
        except:
            return 0

    def click_order_detail(self, order_index=0):
        try:
            orders = self.driver.find_elements(*self.ORDER_LIST)
            if orders and order_index < len(orders):
                orders[order_index].click()
        except:
            pass

    def get_order_status(self):
        try:
            status = self.driver.find_elements(*self.ORDER_STATUS)
            return status[0].text if status else ""
        except:
            return ""

    def cancel_order(self):
        try:
            cancel_btn = self.driver.find_elements(*self.CANCEL_ORDER_BTN)
            if cancel_btn:
                cancel_btn[0].click()
        except:
            pass

    def get_product_count(self):
        try:
            items = self.driver.find_elements(*self.CART_ITEMS)
            return len(items)
        except:
            return 0
