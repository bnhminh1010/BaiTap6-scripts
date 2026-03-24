from pages.login_page import LoginPage


def test_auth_001_verify_login_page_loads_with_required_fields(driver, wait, base_url):
    login_page = LoginPage(driver, wait)
    login_page.open(base_url)

    email_exists = any(driver.find_elements(*locator) for locator in LoginPage.EMAIL_LOCATORS)
    password_exists = any(driver.find_elements(*locator) for locator in LoginPage.PASSWORD_LOCATORS)
    submit_exists = any(driver.find_elements(*locator) for locator in LoginPage.SUBMIT_LOCATORS)

    assert email_exists, "Email input is not found on login page."
    assert password_exists, "Password input is not found on login page."
    assert submit_exists, "Login submit button is not found on login page."


def test_auth_002_verify_login_rejected_with_invalid_password(driver, wait, base_url):
    login_page = LoginPage(driver, wait)
    login_page.open(base_url)
    login_page.login("demouser@microsoft.com", "WrongPassword123")

    assert login_page.has_login_error(), "Expected invalid login error is not displayed."
    assert "/login" in driver.current_url.lower()
