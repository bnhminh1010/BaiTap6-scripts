from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    """Lớp đối tượng đại diện cho trang Giỏ Hàng (Shopping Cart)."""
    
    CART_ITEMS = (By.CSS_SELECTOR, "article.esh-basket-items.row")
    CART_ITEM_NAME = (By.CSS_SELECTOR, "section.esh-basket-item.col-xs-3")
    CART_ITEM_PRICE = (By.CSS_SELECTOR, "section.esh-basket-item.col-xs-2:not(.esh-basket-item--mark)")
    QUANTITY_INPUT = (By.CSS_SELECTOR, ".esh-basket-input[type='number']")
    UPDATE_BUTTON = (By.CSS_SELECTOR, ".esh-basket-checkout[name='updatebutton']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, ".esh-basket-checkout[name='action']")
    TOTAL_PRICE = (By.CSS_SELECTOR, ".esh-basket-item--mark")
    EMPTY_CART_MSG = (By.CSS_SELECTOR, ".esh-catalog-title")
    CONTINUE_SHOPPING_LINK = (By.CSS_SELECTOR, "a[href='/']")

    def add_product(self, product_name, quantity=1):
        # Thông thường việc Thêm vào giỏ được thực hiện trên trang Catalog (Danh mục) hoặc trang Chi tiết sản phẩm
        pass

    def update_quantity(self, index, quantity):
        """Cập nhật số lượng của sản phẩm trong giỏ hàng dựa theo vị trí (index)"""
        quantities = self.driver.find_elements(*self.QUANTITY_INPUT)
        if index < len(quantities):
            quantities[index].clear()
            quantities[index].send_keys(str(quantity))
            self.click(self.UPDATE_BUTTON)

    def update_quantity_by_name(self, product_name, quantity):
        """Tìm sản phẩm theo tên và cập nhật số lượng"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        for i, item in enumerate(items):
            try:
                name = item.find_element(*self.CART_ITEM_NAME).text
                if product_name.lower() in name.lower():
                    self.update_quantity(i, quantity)
                    break
            except:
                pass

    def get_cart_item_count(self):
        """Lấy tổng số dòng sản phẩm đang có trong giỏ hàng"""
        try:
            return len(self.driver.find_elements(*self.QUANTITY_INPUT))
        except:
            return 0

    def get_item_quantity(self, index=0):
        """Lấy số lượng của một sản phẩm trong giỏ hàng tại vị trí index"""
        try:
            quantities = self.driver.find_elements(*self.QUANTITY_INPUT)
            if index < len(quantities):
                return int(quantities[index].get_attribute("value"))
            return 0
        except:
            return 0

    def get_total_price(self):
        """Lấy tổng tiền của toàn bộ giỏ hàng"""
        try:
            # Thường tổng tiền là element cuối cùng mang class này
            total_text = self.driver.find_elements(*self.TOTAL_PRICE)[-1].text  
            return float(total_text.replace("$", "").replace(",", "").strip())
        except:
            return 0.0

    def remove_product(self, index=0):
        """Xoá sản phẩm khỏi giỏ hàng bằng cách set số lượng về 0 và cập nhật"""
        self.update_quantity(index, 0)
