from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    PATH = "/login"

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

    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

    def open(self, base_url):
        self.driver.get(base_url.rstrip("/") + self.PATH)

    def _first_visible(self, locators):
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements[0]
        raise AssertionError(f"No visible element found for locators: {locators}")

    def login(self, email, password):
        email_input = self._first_visible(self.EMAIL_LOCATORS)
        password_input = self._first_visible(self.PASSWORD_LOCATORS)
        submit_btn = self._first_visible(self.SUBMIT_LOCATORS)

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        submit_btn.click()

    def has_login_error(self):
        for locator in self.ERROR_LOCATORS:
            if self.driver.find_elements(*locator):
                return True
        return False

    def wait_until_login_page_loaded(self):
        self.wait.until(EC.presence_of_element_located(self.EMAIL_LOCATORS[0]))
