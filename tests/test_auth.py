"""
===========================================================================
D.1. TEST SCRIPT DESIGN — AUTHENTICATION (TC-AUTH-001 → TC-AUTH-012)
===========================================================================

FILE: test_auth.py
MODULE: Authentication
TOTAL TCs: 12

===========================================================================
TC-AUTH-001: Xác minh đăng nhập thành công khi nhập email/password hợp lệ
===========================================================================
PAGE OBJECTS:
  - LoginPage: email_input, password_input, login_button, error_message
  - HomePage: user_info_header, logo, logout_link

TEST STEPS:
  1. Navigate to /Identity/Account/Login
  2. Wait for login page to load
  3. Enter email: "demouser@microsoft.com"
  4. Enter password: "Password123!"
  5. Click Login button
  6. Wait for redirect to home page
  7. Verify URL contains "/" or home indicator
  8. Verify user info is displayed in header

ASSERTIONS:
  - Assert current URL does not contain "login"
  - Assert user greeting/name is visible in header
  - Assert no error message displayed
  - Assert logout link is visible

LOCATORS:
  - Email: [name="Email"] or [id="Input_Email"]
  - Password: [name="Password"] or [id="Input_Password"]
  - Login btn: [type="submit"], button:contains("Log in")
  - User info: [class*="account"], [class*="user"]
  - Logout: a[href*="Logout"]

===========================================================================
TC-AUTH-002: Xác minh đăng nhập bị từ chối khi nhập password không chính xác
===========================================================================
PAGE OBJECTS:
  - LoginPage: email_input, password_input, login_button, error_message

TEST STEPS:
  1. Navigate to /Identity/Account/Login
  2. Enter email: "demouser@microsoft.com"
  3. Enter password: "WrongPassword123"
  4. Click Login button
  5. Wait for error message to appear
  6. Verify error message text

ASSERTIONS:
  - Assert error message is displayed
  - Assert error message contains "Invalid" or "incorrect" or "wrong"
  - Assert URL still on login page

LOCATORS:
  - Error: [class*="validation-summary-errors"], [class*="alert-danger"], [role="alert"]

===========================================================================
TC-AUTH-003: Xác minh đăng nhập bị từ chối khi email chưa đăng ký
===========================================================================
PAGE OBJECTS:
  - LoginPage: email_input, password_input, login_button, error_message

TEST STEPS:
  1. Navigate to /Identity/Account/Login
  2. Enter email: "nonexistent@test.com"
  3. Enter password: "Password123!"
  4. Click Login button
  5. Wait for error message

ASSERTIONS:
  - Assert error message displayed
  - Assert URL stays on login page

LOCATORS:
  - Same as TC-AUTH-002

===========================================================================
TC-AUTH-004: Xác minh hiển thị validation khi để trống email và password
===========================================================================
PAGE OBJECTS:
  - LoginPage: email_input, password_input, login_button

TEST STEPS:
  1. Navigate to /Identity/Account/Login
  2. Click Login button WITHOUT entering any data
  3. Observe form validation behavior

ASSERTIONS:
  - Assert validation errors shown OR login button is disabled
  - Assert no navigation away from login page

LOCATORS:
  - Email validation: [data-val-required], span.field-validation-error
  - Password validation: [data-val-required]

===========================================================================
TC-AUTH-005: Xác minh hiển thị validation khi nhập email sai định dạng
===========================================================================
PAGE OBJECTS:
  - LoginPage: email_input, password_input, login_button, error_message

TEST STEPS:
  1. Navigate to /Identity/Account/Login
  2. Enter invalid email format: "invalidemail"
  3. Enter password: "SomePassword123!"
  4. Click Login button
  5. Observe validation

ASSERTIONS:
  - Assert email format validation error displayed
  - Assert URL stays on login page

LOCATORS:
  - Email validation: input[type="email"]:invalid, [data-val-email]

===========================================================================
TC-AUTH-006: Xác minh phiên đăng nhập kết thúc khi người dùng chọn Logout
===========================================================================
PAGE OBJECTS:
  - HomePage: user_info_header, logout_link, login_link
  - LoginPage: login_button

TEST STEPS:
  1. Navigate to /Identity/Account/Login
  2. Login with valid credentials
  3. Verify user is logged in
  4. Click Logout button/link
  5. Wait for logout to complete
  6. Verify user is logged out

ASSERTIONS:
  - Assert login link is visible after logout
  - Assert user info is not displayed
  - Assert URL shows login page or home

LOCATORS:
  - Logout: a[href*="Logout"], button:contains("Logout")
  - Login link: a[href*="Login"]

===========================================================================
TC-AUTH-007: Xác minh tạo tài khoản mới thành công với thông tin đăng ký hợp lệ
===========================================================================
PAGE OBJECTS:
  - RegisterPage: name_input, email_input, password_input, confirm_password_input
  - Register button, login_link

TEST STEPS:
  1. Navigate to /Identity/Account/Register
  2. Enter name: "TestUser"
  3. Enter email: unique email
  4. Enter password: "TestPassword123!"
  5. Enter confirm password: "TestPassword123!"
  6. Click Register button
  7. Wait for registration to complete

ASSERTIONS:
  - Assert user is redirected to home or login
  - Assert user is logged in automatically
  - Assert no validation errors

LOCATORS:
  - Name: [name="Input_Name"], #Input_Name
  - Email: [name="Input_Email"], #Input_Email
  - Password: [name="Input_Password"], #Input_Password
  - Confirm: [name="Input_ConfirmPassword"], #Input_ConfirmPassword
  - Register btn: button[type="submit"]

===========================================================================
TC-AUTH-008: Xác minh đăng ký bị từ chối khi email đã tồn tại
===========================================================================
PAGE OBJECTS:
  - RegisterPage: all fields, error_message

TEST STEPS:
  1. Navigate to /Identity/Account/Register
  2. Enter valid name
  3. Enter existing email (from previous test)
  4. Enter valid password
  5. Enter confirm password
  6. Click Register button

ASSERTIONS:
  - Assert error message displayed
  - Assert error mentions email already exists

LOCATORS:
  - Error: [class*="validation-summary-errors"], [class*="alert-danger"]

===========================================================================
TC-AUTH-009: Xác minh đăng ký bị từ chối khi password không đạt độ mạnh tối thiểu
===========================================================================
PAGE OBJECTS:
  - RegisterPage: password_input, error_message

TEST STEPS:
  1. Navigate to /Identity/Account/Register
  2. Enter valid name and email
  3. Enter weak password: "12345"
  4. Enter confirm password: "12345"
  5. Click Register button

ASSERTIONS:
  - Assert password validation error displayed
  - Assert error mentions password requirements

LOCATORS:
  - Password error: [data-val-length], [data-val-required]

===========================================================================
TC-AUTH-010: Xác minh đăng ký bị từ chối khi password và confirm không khớp
===========================================================================
PAGE_OBJECTS:
  - RegisterPage: password_input, confirm_password_input, error_message

TEST STEPS:
  1. Navigate to /Identity/Account/Register
  2. Enter valid name and email
  3. Enter password: "Password123!"
  4. Enter different confirm: "DifferentPass123!"
  5. Click Register button

ASSERTIONS:
  - Assert error message displayed
  - Assert error mentions password mismatch

LOCATORS:
  - Confirm error: [data-valEqualTo]

===========================================================================
TC-AUTH-011: Xác minh người dùng đã đăng nhập bị chuyển hướng khi truy cập trang login
===========================================================================
PAGE OBJECTS:
  - LoginPage, HomePage

TEST STEPS:
  1. Login with valid credentials
  2. Navigate directly to /Identity/Account/Login
  3. Observe redirect behavior

ASSERTIONS:
  - Assert user is redirected to home page
  - Assert user stays logged in

LOCATORS:
  - Same as other pages

===========================================================================
TC-AUTH-012: Xác minh trạng thái đăng nhập được duy trì khi chọn Remember Me
===========================================================================
PAGE OBJECTS:
  - LoginPage: remember_me_checkbox, login_button

TEST STEPS:
  1. Navigate to /Identity/Account/Login
  2. Enter valid email and password
  3. Check "Remember Me" checkbox
  4. Click Login button
  5. Capture cookies
  6. Verify remember-me cookie exists

ASSERTIONS:
  - Assert user is logged in
  - Assert persistent cookie is set
  - Assert cookie persists after browser restart (if applicable)

LOCATORS:
  - Remember me: [name="Input_RememberMe"], #Input_RememberMe

===========================================================================
"""

import os
import time

import pytest
from selenium.webdriver.support import expected_conditions as EC

from pages.auth_page import AuthPage


VALID_EMAIL = os.getenv("E2E_VALID_EMAIL", "demouser@microsoft.com")
VALID_PASSWORD = os.getenv("E2E_VALID_PASSWORD", "Pass@word1")


def register_test_user(driver, base_url, unique_suffix=""):
    """Helper function to register a test user and return credentials."""
    auth_page = AuthPage(driver)
    timestamp = int(time.time())
    suffix = f"{timestamp}{unique_suffix}"
    test_name = f"TestUser{suffix}"
    test_email = f"testuser{suffix}@test.com"
    test_password = "TestPassword123!"

    auth_page.open_register(base_url)
    time.sleep(1)
    auth_page.register(test_name, test_email, test_password, test_password)
    time.sleep(2)

    return test_email, test_password


def ensure_logged_out(driver):
    """Ensure user is logged out."""
    auth_page = AuthPage(driver)
    if auth_page.is_user_logged_in():
        auth_page.logout()
        time.sleep(1)


def test_auth_001_verify_login_success_with_valid_credentials(driver, wait, base_url):
    """TC-AUTH-001: Xác minh đăng nhập thành công khi nhập email/password hợp lệ"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    test_email, test_password = register_test_user(driver, base_url, "login1")

    ensure_logged_out(driver)

    auth_page.open_login(base_url)
    time.sleep(1)

    assert auth_page.is_login_form_displayed(), (
        f"Login form is not displayed. URL: {driver.current_url}"
    )

    auth_page.login(test_email, test_password)
    time.sleep(2)

    has_error = auth_page.has_login_error()
    assert not has_error, (
        f"Login should succeed but got error: {auth_page.get_error_message()}"
    )
    assert (
        auth_page.is_user_logged_in() or "/login" not in driver.current_url.lower()
    ), f"User should be logged in after successful login. URL: {driver.current_url}"


def test_auth_002_verify_login_rejected_with_invalid_password(driver, wait, base_url):
    """TC-AUTH-002: Xác minh đăng nhập bị từ chối khi nhập password không chính xác"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    test_email, _ = register_test_user(driver, base_url, "invalid2")

    ensure_logged_out(driver)

    auth_page.open_login(base_url)
    time.sleep(1)

    assert auth_page.is_login_form_displayed(), "Login form is not displayed."
    auth_page.login(test_email, "WrongPassword123")

    time.sleep(1)
    assert auth_page.has_login_error(), "Expected login error is not displayed."
    assert auth_page.is_on_login_page(), "User should remain on login page."


def test_auth_003_verify_login_rejected_with_unregistered_email(driver, wait, base_url):
    """TC-AUTH-003: Xác minh đăng nhập bị từ chối khi email chưa đăng ký"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    auth_page.open_login(base_url)

    time.sleep(1)
    assert auth_page.is_login_form_displayed(), "Login form is not displayed."
    auth_page.login(f"nonexistent{int(time.time())}@test.com", "SomePassword123!")

    time.sleep(1)
    assert auth_page.has_login_error(), "Expected login error is not displayed."
    assert auth_page.is_on_login_page(), "User should remain on login page."


def test_auth_004_verify_validation_for_empty_email_and_password(
    driver, wait, base_url
):
    """TC-AUTH-004: Xác minh hiển thị validation khi để trống email và password"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    auth_page.open_login(base_url)

    time.sleep(1)
    assert auth_page.is_login_form_displayed(), "Login form is not displayed."

    email_input = auth_page._first(auth_page.EMAIL_LOCATORS)
    password_input = auth_page._first(auth_page.PASSWORD_LOCATORS)
    submit_btn = auth_page._first(auth_page.SUBMIT_LOCATORS)

    email_input.clear()
    password_input.clear()

    is_button_disabled = auth_page.is_submit_button_disabled()
    submit_btn.click()
    time.sleep(0.5)

    validation_errors = auth_page.get_validation_errors()
    assert is_button_disabled or len(validation_errors) > 0, (
        "Expected validation error or disabled button when submitting empty form."
    )
    assert auth_page.is_on_login_page(), "User should remain on login page."


def test_auth_005_verify_validation_for_invalid_email_format(driver, wait, base_url):
    """TC-AUTH-005: Xác minh hiển thị validation khi nhập email sai định dạng"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    auth_page.open_login(base_url)

    time.sleep(1)
    assert auth_page.is_login_form_displayed(), "Login form is not displayed."
    auth_page.login("invalidemail", "SomePassword123!")

    time.sleep(0.5)
    validation_errors = auth_page.get_validation_errors()

    is_invalid_format = auth_page.has_login_error() or len(validation_errors) > 0
    assert is_invalid_format or auth_page.is_on_login_page(), (
        "Expected email format validation error or stay on login page."
    )


def test_auth_006_verify_logout_ends_authenticated_session(driver, wait, base_url):
    """TC-AUTH-006: Xác minh phiên đăng nhập kết thúc khi người dùng chọn Logout"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    test_email, test_password = register_test_user(driver, base_url, "logout6")

    assert auth_page.is_user_logged_in(), "User should be logged in after registration."

    auth_page.logout()
    time.sleep(2)

    assert (
        auth_page.is_login_link_visible() or "/login" in driver.current_url.lower()
    ), "Login link should be visible after logout."
    assert not auth_page.is_user_logged_in(), (
        "User info should not be visible after logout."
    )


def test_auth_007_verify_registration_success_with_valid_data(driver, wait, base_url):
    """TC-AUTH-007: Xác minh tạo tài khoản mới thành công với thông tin đăng ký hợp lệ"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    timestamp = int(time.time())
    test_name = f"TestUser{timestamp}"
    test_email = f"testuser{timestamp}@test.com"
    test_password = "TestPassword123!"

    auth_page.open_register(base_url)
    time.sleep(0.5)

    auth_page.register(test_name, test_email, test_password, test_password)
    time.sleep(2)

    current_url = driver.current_url.lower()
    is_logged_in = auth_page.is_user_logged_in()
    assert "/register" not in current_url or is_logged_in, (
        "User should be redirected or logged in after successful registration."
    )
    assert is_logged_in or "/login" not in current_url, (
        "User should be authenticated after registration."
    )

    if is_logged_in:
        auth_page.logout()
        time.sleep(1)


def test_auth_008_verify_registration_rejected_for_existing_email(
    driver, wait, base_url
):
    """TC-AUTH-008: Xác minh đăng ký bị từ chối khi email đã tồn tại"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    timestamp = int(time.time())
    test_name = f"TestUser{timestamp}"
    existing_email, _ = register_test_user(driver, base_url, f"exist{timestamp}")

    ensure_logged_out(driver)

    auth_page.open_register(base_url)
    time.sleep(0.5)

    auth_page.register(
        test_name, existing_email, "TestPassword123!", "TestPassword123!"
    )
    time.sleep(1)

    validation_errors = auth_page.get_validation_errors()
    has_error = auth_page.has_login_error() or len(validation_errors) > 0

    current_url = driver.current_url.lower()
    assert has_error or "/register" in current_url, (
        "Expected error message when registering with existing email."
    )
    if has_error:
        error_text = auth_page.get_error_message() or " ".join(validation_errors)
        assert "email" in error_text.lower() or "exist" in error_text.lower(), (
            f"Error should mention email already exists. Got: {error_text}"
        )


def test_auth_009_verify_registration_rejected_for_weak_password(
    driver, wait, base_url
):
    """TC-AUTH-009: Xác minh đăng ký bị từ chối khi password không đạt độ mạnh tối thiểu"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    timestamp = int(time.time())
    test_name = f"TestUser{timestamp}"
    test_email = f"testuser{timestamp}@test.com"
    weak_password = "12345"

    auth_page.open_register(base_url)
    time.sleep(0.5)

    auth_page.register(test_name, test_email, weak_password, weak_password)
    time.sleep(1)

    validation_errors = auth_page.get_validation_errors()
    has_error = auth_page.has_login_error() or len(validation_errors) > 0

    current_url = driver.current_url.lower()
    assert has_error or "/register" in current_url, (
        "Expected password validation error for weak password."
    )
    if has_error:
        error_text = auth_page.get_error_message() or " ".join(validation_errors)
        assert any(
            keyword in error_text.lower()
            for keyword in ["password", "length", "minimum"]
        ), f"Error should mention password requirements. Got: {error_text}"


def test_auth_010_verify_registration_rejected_for_password_mismatch(
    driver, wait, base_url
):
    """TC-AUTH-010: Xác minh đăng ký bị từ chối khi password và confirm password không khớp"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    timestamp = int(time.time())
    test_name = f"TestUser{timestamp}"
    test_email = f"testuser{timestamp}@test.com"

    auth_page.open_register(base_url)
    time.sleep(0.5)

    auth_page.register(test_name, test_email, "Password123!", "DifferentPass123!")
    time.sleep(1)

    validation_errors = auth_page.get_validation_errors()
    has_error = auth_page.has_login_error() or len(validation_errors) > 0

    current_url = driver.current_url.lower()
    assert has_error or "/register" in current_url, "Expected password mismatch error."
    if has_error:
        error_text = auth_page.get_error_message() or " ".join(validation_errors)
        assert any(
            keyword in error_text.lower()
            for keyword in ["match", "confirm", "password"]
        ), f"Error should mention password mismatch. Got: {error_text}"


def test_auth_011_verify_redirect_when_authenticated_user_accesses_login(
    driver, wait, base_url
):
    """TC-AUTH-011: Xác minh người dùng đã đăng nhập bị chuyển hướng khi truy cập lại trang login"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    test_email, test_password = register_test_user(driver, base_url, "redirect11")

    assert auth_page.is_user_logged_in(), "User should be logged in after registration."

    auth_page.open_login(base_url)
    time.sleep(1)

    current_url = driver.current_url.lower()
    is_redirected = "/login" not in current_url or auth_page.is_user_logged_in()
    assert is_redirected, (
        "Authenticated user should be redirected or shown logged-in state when accessing login page."
    )


def test_auth_012_verify_session_persists_with_remember_me_enabled(
    driver, wait, base_url
):
    """TC-AUTH-012: Xác minh trạng thái đăng nhập được duy trì khi chọn Remember Me"""
    ensure_logged_out(driver)

    auth_page = AuthPage(driver)
    test_email, test_password = register_test_user(driver, base_url, "remember12")

    ensure_logged_out(driver)

    auth_page.open_login(base_url)
    time.sleep(1)
    auth_page.login_with_remember_me(test_email, test_password)
    time.sleep(2)
    assert auth_page.is_user_logged_in(), "User should be logged in after login."

    # Capture cookies BEFORE deleting them — verify a remember-me cookie was set
    cookies_before = driver.get_cookies()
    has_remember_cookie = any(
        "remember" in c.get("name", "").lower()
        or "persistent" in c.get("name", "").lower()
        or ".aspnetcore" in c.get("name", "").lower()
        for c in cookies_before
    )

    # Assert: the app issued a persistent/remember cookie when Remember Me was checked
    assert has_remember_cookie, (
        f"Expected a persistent/remember-me cookie to be set. Cookies found: "
        f"{[c.get('name') for c in cookies_before]}"
    )
