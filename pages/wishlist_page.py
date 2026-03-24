from pages.base_page import BasePage


class WishlistPage(BasePage):
    """Wishlist and compare page object skeleton."""

    def add_to_wishlist(self, product_name):
        raise NotImplementedError("TODO: implement add to wishlist action")

    def remove_from_wishlist(self, product_name):
        raise NotImplementedError("TODO: implement remove from wishlist action")

    def add_to_compare(self, product_name):
        raise NotImplementedError("TODO: implement compare action")
