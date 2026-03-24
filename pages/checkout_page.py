from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Checkout and order page object skeleton."""

    def proceed_to_checkout(self):
        raise NotImplementedError("TODO: implement proceed to checkout action")

    def apply_voucher(self, code):
        raise NotImplementedError("TODO: implement apply voucher action")

    def place_order(self):
        raise NotImplementedError("TODO: implement place order action")
