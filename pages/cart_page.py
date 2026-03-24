from pages.base_page import BasePage


class CartPage(BasePage):
    """Shopping cart page object skeleton."""

    def add_product(self, product_name, quantity=1):
        raise NotImplementedError("TODO: implement add product action")

    def update_quantity(self, product_name, quantity):
        raise NotImplementedError("TODO: implement update quantity action")

    def remove_product(self, product_name):
        raise NotImplementedError("TODO: implement remove product action")
