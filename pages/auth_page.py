import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

from pages.base_page import BasePage


class AuthPage(BasePage):
    LOGIN_PATH = "/Identity/Account/Login"
    REGISTER_PATH = "/Identity/Account/Register"

    # --- Login form locators ---
    EMAIL_LOCATORS = [
        (By.ID, "Input_Email"),
        (By.NAME, "Input.Email"),
        (By.CSS_SELECTOR, "input[type='email']"),
    ]
    PASSWORD_LOCATORS = [
        (By.ID, "Input_Password"),
        (By.NAME, "Input.Password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ]
    SUBMIT_LOCATORS = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(.,'Log in') or contains(.,'Login') or contains(.,'Register')]"),
    ]

    # --- Error / validation locators ---
    ERROR_LOCATORS = [
        (By.CSS_SELECTOR, ".validation-summary-errors"),
        (By.CSS_SELECTOR, ".text-danger"),
        (By.CSS_SELECTOR, "[role='alert']"),
        (By.XPATH, "//*[contains(@class,'validation-summary-errors')]"),
        (By.XPATH, "//*[contains(text(),'Invalid login attempt')]"),
        (By.XPATH, "//*[contains(text(),'error') or contains(text(),'Error')]"),
    ]

    # --- Remember Me locator ---
    REMEMBER_ME_LOCATORS = [
        (By.ID, "Input_RememberMe"),
        (By.NAME, "Input.RememberMe"),
        (By.CSS_SELECTOR, "input[type='checkbox']"),
    ]

    # --- User info locators (confirmed from live site: .esh-identity-name) ---
    USER_INFO_LOCATORS = [
        (By.CSS_SELECTOR, ".esh-identity-name"),
        (By.CSS_SELECTOR, ".esh-identity-section"),
        (By.CSS_SELECTOR, ".esh-identity"),
    ]

    # --- Logout: the logout link triggers #logoutForm.submit() ---
    LOGOUT_LINK_LOCATORS = [
        (By.XPATH, "//a[contains(@href,'javascript') and contains(.,'Log Out')]"),
        (By.XPATH, "//a[contains(.,'Log Out') or contains(.,'Logout') or contains(.,'log out')]"),
    ]
    LOGOUT_FORM_ID = "logoutForm"

    # --- Login link (when logged out) ---
    LOGIN_LINK_LOCATORS = [
        (By.XPATH, "//a[contains(@href,'/login') or contains(@href,'/Login')]"),
        (By.XPATH, "//a[contains(text(),'Login') or contains(text(),'Log in')]"),
    ]

    # --- Register form locators ---
    NAME_INPUT_LOCATORS = [
        (By.ID, "Input_Name"),
        (By.NAME, "Input.Name"),
        (By.XPATH, "//input[contains(@id,'Name') or contains(@name,'Name')]"),
    ]
    CONFIRM_PASSWORD_LOCATORS = [
        (By.ID, "Input_ConfirmPassword"),
        (By.NAME, "Input.ConfirmPassword"),
    ]
    REGISTER_BUTTON_LOCATORS = [
        (By.XPATH, "//button[contains(.,'Register')]"),
        (By.CSS_SELECTOR, "button[type='submit']"),
    ]

    # ------------------------------------------------------------------ helpers

    def open_login(self, base_url):
        self.open(base_url.rstrip("/") + self.LOGIN_PATH)

    def open_register(self, base_url):
        self.open(base_url.rstrip("/") + self.REGISTER_PATH)

    def _first(self, locators, visible_only=True):
        """Return the first element that is both displayed AND enabled.
        If visible_only=True (default), never return a hidden/disabled element.
        """
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            for el in elements:
                try:
                    if el.is_displayed() and el.is_enabled():
                        return el
                except Exception:
                    continue
        return None

    def _first_any(self, locators):
        """Return first element regardless of visibility (for read-only checks)."""
        for locator in locators:
            elements = self.driver.find_elements(*locator)
            if elements:
                return elements[0]
        return None

    # ------------------------------------------------------------------ actions

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
            raise AssertionError(
                f"Login form elements not found. URL: {self.driver.current_url}"
            )

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        submit_btn.click()

    def login_with_remember_me(self, email, password):
        email_input = self._first(self.EMAIL_LOCATORS)
        password_input = self._first(self.PASSWORD_LOCATORS)
        remember_me = self._first(self.REMEMBER_ME_LOCATORS)
        submit_btn = self._first(self.SUBMIT_LOCATORS)

        if not email_input or not password_input or not submit_btn:
            raise AssertionError("Login form elements not found.")

        email_input.clear()
        email_input.send_keys(email)
        password_input.clear()
        password_input.send_keys(password)
        if remember_me and not remember_me.is_selected():
            remember_me.click()
        submit_btn.click()

    # ------------------------------------------------------------------ logout

    def logout(self):
        """
        eShopOnWeb logout works by submitting a hidden form (#logoutForm).
        The 'Log Out' anchor calls: javascript:document.getElementById('logoutForm').submit()
        After logout the app redirects to '/' (home), NOT '/login'.
        """
        # Capture current URL before logout to detect navigation
        url_before = self.driver.current_url

        # Try clicking the visible Log Out link first (it triggers JS form submit)
        logout_link = self._first(self.LOGOUT_LINK_LOCATORS)
        if logout_link:
            logout_link.click()
        else:
            # Fallback: submit the logout form via JavaScript
            try:
                self.driver.execute_script(
                    "var f = document.getElementById('logoutForm'); if(f) f.submit();"
                )
            except Exception:
                pass

        # Wait until the URL actually changes (page navigated away) OR login page appears
        try:
            self.wait.until(
                lambda d: d.current_url != url_before
                or "/Identity/Account/Login" in d.current_url
            )
        except Exception:
            time.sleep(2)

        # Wait for user info to disappear (indicating logout was successful)
        try:
            self.wait.until(lambda d: not self.is_user_logged_in())
        except Exception:
            time.sleep(2)

        # Extra wait to let the new page render fully
        time.sleep(1)

    # ------------------------------------------------------------------ assertions / getters

    def has_login_error(self):
        for locator in self.ERROR_LOCATORS:
            elements = self.driver.find_elements(*locator)
            for el in elements:
                try:
                    if el.is_displayed() and el.text.strip():
                        return True
                except Exception:
                    continue
        return False

    def get_error_message(self):
        for locator in self.ERROR_LOCATORS:
            elements = self.driver.find_elements(*locator)
            for el in elements:
                try:
                    if el.is_displayed() and el.text.strip():
                        return el.text
                except Exception:
                    continue
        return None

    def is_on_login_page(self):
        return self.LOGIN_PATH.lower() in self.driver.current_url.lower()

    def is_user_logged_in(self):
        """Check if user is logged in by looking for user info (not Login/Log in text)."""
        for locator in self.USER_INFO_LOCATORS:
            elements = self.driver.find_elements(*locator)
            for el in elements:
                try:
                    if el.is_displayed() and el.text.strip():
                        text = el.text.strip().lower()
                        # Exclude login/logout buttons - these indicate NOT logged in
                        if "login" not in text and "log in" not in text and "logout" not in text and "log out" not in text:
                            return True
                except Exception:
                    continue
        return False

    def is_login_link_visible(self):
        """Check if login link is visible (without requiring is_enabled check for anchors)."""
        for locator in self.LOGIN_LINK_LOCATORS:
            elements = self.driver.find_elements(*locator)
            for el in elements:
                try:
                    if el.is_displayed():
                        return True
                except Exception:
                    continue
        return False

    def register(self, name, email, password, confirm_password):
        name_input = self._first(self.NAME_INPUT_LOCATORS)
        email_input = self._first(self.EMAIL_LOCATORS)
        password_input = self._first(self.PASSWORD_LOCATORS)
        confirm_input = self._first(self.CONFIRM_PASSWORD_LOCATORS)
        register_btn = self._first(self.REGISTER_BUTTON_LOCATORS)

        if name_input:
            name_input.clear()
            name_input.send_keys(name)
        if email_input:
            email_input.clear()
            email_input.send_keys(email)
        if password_input:
            password_input.clear()
            password_input.send_keys(password)
        if confirm_input:
            confirm_input.clear()
            confirm_input.send_keys(confirm_password)

        if register_btn:
            register_btn.click()
        else:
            submit_btn = self._first(self.SUBMIT_LOCATORS)
            if submit_btn:
                submit_btn.click()

    def get_validation_errors(self):
        errors = []
        for locator in self.ERROR_LOCATORS:
            elements = self.driver.find_elements(*locator)
            for el in elements:
                try:
                    if el.is_displayed() and el.text.strip():
                        errors.append(el.text.strip())
                except Exception:
                    continue
        return errors

    def is_submit_button_disabled(self):
        submit_btn = self._first_any(self.SUBMIT_LOCATORS)
        if submit_btn:
            return not submit_btn.is_enabled()
        return True

    def get_page_title(self):
        return self.driver.title
