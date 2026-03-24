from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AuthPage(BasePage):
    """Authentication page object skeleton."""

    LOGIN_PATH = "/login"

    EMAIL_LOCATORS = [
        (By.ID, "Input_Email"),
        (By.NAME, "Email"),
        (By.CSS_SELECTOR, "input[type='email']"),
    ]
    PASSWORD_LOCATORS = [
        (By.ID, "Input_Password"),
        (By.NAME, "Password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]
    SUBMIT_LOCATORS = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(.,'Log in') or contains(.,'Login')]"),
    ]
    ERROR_LOCATORS = [
        (By.CSS_SELECTOR, ".validation-summary-errors"),
        (By.CSS_SELECTOR, "[role='alert']"),
        (By.XPATH, "//*[contains(text(),'Invalid login attempt')]"),
    ]

    def open_login(self, base_url):
        self.open(base_url.rstrip("/") + self.LOGIN_PATH)

    def _first(self, locators):
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements[0]
        return None

    def is_login_form_displayed(self):
        return (
            self._first(self.EMAIL_LOCATORS) is not None
            and self._first(self.PASSWORD_LOCATORS) is not None
            and self._first(self.SUBMIT_LOCATORS) is not None
        )

    def login(self, email, password):
        email_input = self._first(self.EMAIL_LOCATORS)
        password_input = self._first(self.PASSWORD_LOCATORS)
        submit_btn = self._first(self.SUBMIT_LOCATORS)

        if not email_input or not password_input or not submit_btn:
            raise AssertionError("Login form elements are not available.")

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        submit_btn.click()

    def has_login_error(self):
        return any(self.driver.find_elements(*locator) for locator in self.ERROR_LOCATORS)

    def is_on_login_page(self):
        return self.LOGIN_PATH in self.driver.current_url.lower()

    def logout(self):
        raise NotImplementedError("TODO: implement logout action")

    def register(self, name, email, password, confirm_password):
        raise NotImplementedError("TODO: implement register action")
