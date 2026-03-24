from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CatalogPage(BasePage):
    # --- Locators thực tế từ eShopOnWeb ---
    SEARCH_INPUT = (By.NAME, "searchString")
    SEARCH_BUTTON = (By.CLASS_NAME, "esh-catalog-send")
    BRAND_FILTER = (By.ID, "CatalogModel_BrandFilterApplied")
    TYPE_FILTER = (By.ID, "CatalogModel_TypesFilterApplied")
    PRODUCT_ITEMS = (By.CLASS_NAME, "esh-catalog-item")
    PRODUCT_ITEM = (By.CSS_SELECTOR, ".esh-catalog-item")
    PRODUCT_NAMES = (By.CLASS_NAME, "esh-catalog-name")
    PRODUCT_PRICES = (By.CLASS_NAME, "esh-catalog-price")

    # Locators cho Phân trang (Pagination)
    PAGINATION_NEXT = (By.ID, "Next")
    PAGINATION_PREV = (By.ID, "Previous")
    PAGER_INFO = (By.CLASS_NAME, "esh-pager-item")

    # Sort dropdown
    SORT_DROPDOWN = (By.ID, "CatalogModel_SortOrder")

    def wait_for_catalog_load(self):
        """Đợi trang catalog load xong"""
        try:
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located(self.PRODUCT_ITEMS)
            )
        except:
            pass

    def search(self, keyword):
        """TC-CAT-002, 003, 004: Tìm kiếm sản phẩm"""
        try:
            search_input = self.driver.find_element(*self.SEARCH_INPUT)
            search_input.clear()
            search_input.send_keys(keyword)
            self.click(self.SEARCH_BUTTON)
            self.wait_for_catalog_load()
        except:
            pass

    def apply_category_filter(self, category_text):
        """TC-CAT-005: Lọc theo loại sản phẩm (Dropdown)"""
        try:
            select = Select(self.driver.find_element(*self.TYPE_FILTER))
            select.select_by_visible_text(category_text)
            self.click(self.SEARCH_BUTTON)
            self.wait_for_catalog_load()
        except:
            pass

    def apply_brand_filter(self, brand_text):
        """TC-CAT-006: Lọc theo thương hiệu (Dropdown)"""
        try:
            select = Select(self.driver.find_element(*self.BRAND_FILTER))
            select.select_by_visible_text(brand_text)
            self.click(self.SEARCH_BUTTON)
            self.wait_for_catalog_load()
        except:
            pass

    def sort_by_price_ascending(self):
        """TC-CAT-008: Sắp xếp giá tăng dần"""
        try:
            select = Select(self.driver.find_element(*self.SORT_DROPDOWN))
            select.select_by_value("1")
            self.click(self.SEARCH_BUTTON)
            self.wait_for_catalog_load()
        except:
            pass

    def sort_by_price_descending(self):
        """TC-CAT-009: Sắp xếp giá giảm dần"""
        try:
            select = Select(self.driver.find_element(*self.SORT_DROPDOWN))
            select.select_by_value("2")
            self.click(self.SEARCH_BUTTON)
            self.wait_for_catalog_load()
        except:
            pass

    def go_to_next_page(self):
        """TC-CAT-009, 011: Chuyển trang kế tiếp"""
        try:
            next_btn = self.driver.find_element(*self.PAGINATION_NEXT)
            if "is-disabled" not in next_btn.get_attribute("class"):
                next_btn.click()
                self.wait_for_catalog_load()
        except:
            pass

    def go_to_prev_page(self):
        """Chuyển về trang trước"""
        try:
            prev_btn = self.driver.find_element(*self.PAGINATION_PREV)
            if "is-disabled" not in prev_btn.get_attribute("class"):
                prev_btn.click()
                self.wait_for_catalog_load()
        except:
            pass

    def click_first_product(self):
        """Click vào sản phẩm đầu tiên"""
        try:
            products = self.driver.find_elements(*self.PRODUCT_ITEM)
            if products:
                products[0].click()
        except:
            pass

    def get_product_names(self):
        """Lấy danh sách tên sản phẩm"""
        try:
            names = self.driver.find_elements(*self.PRODUCT_NAMES)
            return [name.text for name in names if name.text]
        except:
            return []

    def get_product_prices(self):
        """Lấy danh sách giá sản phẩm"""
        try:
            prices = self.driver.find_elements(*self.PRODUCT_PRICES)
            return [price.text for price in prices if price.text]
        except:
            return []

    def get_product_count(self):
        """Lấy số lượng sản phẩm đang hiển thị trên lưới"""
        try:
            return len(self.driver.find_elements(*self.PRODUCT_ITEMS))
        except:
            return 0

    def get_pager_text(self):
        """Lấy thông tin trạng thái phân trang (Page X of Y)"""
        try:
            pager = self.driver.find_element(*self.PAGER_INFO)
            return pager.text if pager else ""
        except:
            return ""
