from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage


class WishlistPage(BasePage):
    WISHLIST_LINK = (By.CSS_SELECTOR, "a[href*='Wishlist'], a[href*='wishlist']")
    WISHLIST_ITEMS = (
        By.CSS_SELECTOR,
        ".esh-wishlist-item, .wishlist-item, [class*='wishlist']",
    )
    WISHLIST_EMPTY = (
        By.CSS_SELECTOR,
        "[class*='empty'], [class*='Empty'], .alert-warning",
    )
    WISHLIST_COUNT_BADGE = (
        By.CSS_SELECTOR,
        "[class*='wishlist-count'], [id*='wishlist']",
    )

    WISHLIST_BUTTON = (
        By.CSS_SELECTOR,
        "[class*='wishlist'], [data-action='wishlist'], button[title*='Wish']",
    )
    ADD_TO_BASKET_BTN = (
        By.CSS_SELECTOR,
        ".esh-catalog-button, button.btn-add-basket, [class*='add-to-cart']",
    )
    REMOVE_BTN = (
        By.CSS_SELECTOR,
        "[class*='remove'], [class*='delete'], button[title*='Remove']",
    )

    COMPARE_LINK = (By.CSS_SELECTOR, "a[href*='Compare'], a[href*='compare']")
    COMPARE_ITEMS = (By.CSS_SELECTOR, ".compare-item, [class*='compare']")
    COMPARE_TABLE = (By.CSS_SELECTOR, "table.compare, .compare-table")

    PRODUCT_NAME = (By.CLASS_NAME, "esh-catalog-name")
    PRODUCT_PRICE = (By.CLASS_NAME, "esh-catalog-price")
    PRODUCT_ITEMS = (By.CLASS_NAME, "esh-catalog-item")

    HEART_ICON = (
        By.CSS_SELECTOR,
        "button[aria-label*='Add to wishlist'], i.fa-heart, span.fa-heart",
    )

    def wait_for_page_load(self):
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.PRODUCT_ITEMS)
            )
        except:
            pass

    def has_wishlist_function(self):
        try:
            wishlist_links = self.driver.find_elements(
                By.CSS_SELECTOR, "a[href*='wishlist'], a[href*='Wishlist']"
            )
            wishlist_buttons = self.driver.find_elements(
                By.CSS_SELECTOR, "[class*='wishlist'], [data-action*='wishlist']"
            )
            return len(wishlist_links) > 0 or len(wishlist_buttons) > 0
        except:
            return False

    def has_compare_function(self):
        try:
            compare_links = self.driver.find_elements(
                By.CSS_SELECTOR, "a[href*='compare'], a[href*='Compare']"
            )
            return len(compare_links) > 0
        except:
            return False

    def navigate_to_wishlist(self):
        try:
            wishlist_link = self.driver.find_elements(*self.WISHLIST_LINK)
            if wishlist_link:
                wishlist_link[0].click()
                self.wait_for_page_load()
        except:
            self.driver.get(self.driver.current_url + "/Wishlist")

    def get_wishlist_count(self):
        try:
            items = self.driver.find_elements(*self.WISHLIST_ITEMS)
            return len(items)
        except:
            return 0

    def is_wishlist_empty(self):
        try:
            empty_msg = self.driver.find_elements(*self.WISHLIST_EMPTY)
            items = self.driver.find_elements(*self.WISHLIST_ITEMS)
            return len(empty_msg) > 0 or len(items) == 0
        except:
            return True

    def get_product_names(self):
        try:
            names = self.driver.find_elements(*self.PRODUCT_NAME)
            return [name.text for name in names if name.text]
        except:
            return []

    def get_product_prices(self):
        try:
            prices = self.driver.find_elements(*self.PRODUCT_PRICE)
            return [price.text for price in prices if price.text]
        except:
            return []

    def add_product_to_wishlist(self, product_index=0):
        try:
            products = self.driver.find_elements(*self.PRODUCT_ITEMS)
            if products and product_index < len(products):
                product = products[product_index]
                wishlist_btns = product.find_elements(
                    By.CSS_SELECTOR, "[class*='wishlist'], button[data-action*='wish']"
                )
                if wishlist_btns:
                    wishlist_btns[0].click()
                else:
                    heart_icon = product.find_elements(
                        By.CSS_SELECTOR,
                        "i.fa-heart, span.fa-heart, button[aria-label*='wish']",
                    )
                    if heart_icon:
                        heart_icon[0].click()
        except:
            pass

    def remove_first_product_from_wishlist(self):
        try:
            remove_btns = self.driver.find_elements(*self.REMOVE_BTN)
            if remove_btns:
                remove_btns[0].click()
            else:
                items = self.driver.find_elements(*self.WISHLIST_ITEMS)
                if items:
                    first_item = items[0]
                    delete_btn = first_item.find_elements(
                        By.CSS_SELECTOR, "[class*='remove'], [class*='delete']"
                    )
                    if delete_btn:
                        delete_btn[0].click()
        except:
            pass

    def add_first_product_to_cart(self):
        try:
            add_btns = self.driver.find_elements(*self.ADD_TO_BASKET_BTN)
            if add_btns:
                add_btns[0].click()
        except:
            pass

    def navigate_to_compare(self):
        try:
            compare_link = self.driver.find_elements(*self.COMPARE_LINK)
            if compare_link:
                compare_link[0].click()
                self.wait_for_page_load()
        except:
            pass

    def get_compare_items_count(self):
        try:
            items = self.driver.find_elements(*self.COMPARE_ITEMS)
            return len(items)
        except:
            return 0

    def get_product_count(self):
        try:
            return len(self.driver.find_elements(*self.PRODUCT_ITEMS))
        except:
            return 0
