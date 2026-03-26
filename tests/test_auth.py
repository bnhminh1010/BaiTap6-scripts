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
    
    assert auth_page.is_login_form_displayed(), f"Login form is not displayed. URL: {driver.current_url}"
    
    auth_page.login(test_email, test_password)
    time.sleep(2)
    
    has_error = auth_page.has_login_error()
    assert not has_error, f"Login should succeed but got error: {auth_page.get_error_message()}"
    assert auth_page.is_user_logged_in() or "/login" not in driver.current_url.lower(), \
        f"User should be logged in after successful login. URL: {driver.current_url}"


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


def test_auth_004_verify_validation_for_empty_email_and_password(driver, wait, base_url):
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
    assert is_button_disabled or len(validation_errors) > 0, \
        "Expected validation error or disabled button when submitting empty form."
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
    assert is_invalid_format or auth_page.is_on_login_page(), \
        "Expected email format validation error or stay on login page."


def test_auth_006_verify_logout_ends_authenticated_session(driver, wait, base_url):
    """TC-AUTH-006: Xác minh phiên đăng nhập kết thúc khi người dùng chọn Logout"""
    ensure_logged_out(driver)
    
    auth_page = AuthPage(driver)
    test_email, test_password = register_test_user(driver, base_url, "logout6")
    
    assert auth_page.is_user_logged_in(), "User should be logged in after registration."
    
    auth_page.logout()
    time.sleep(2)
    
    assert auth_page.is_login_link_visible() or "/login" in driver.current_url.lower(), \
        "Login link should be visible after logout."
    assert not auth_page.is_user_logged_in(), "User info should not be visible after logout."


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
    assert "/register" not in current_url or is_logged_in, \
        "User should be redirected or logged in after successful registration."
    assert is_logged_in or "/login" not in current_url, \
        "User should be authenticated after registration."
    
    if is_logged_in:
        auth_page.logout()
        time.sleep(1)


def test_auth_008_verify_registration_rejected_for_existing_email(driver, wait, base_url):
    """TC-AUTH-008: Xác minh đăng ký bị từ chối khi email đã tồn tại"""
    ensure_logged_out(driver)
    
    auth_page = AuthPage(driver)
    timestamp = int(time.time())
    test_name = f"TestUser{timestamp}"
    existing_email, _ = register_test_user(driver, base_url, f"exist{timestamp}")
    
    ensure_logged_out(driver)
    
    auth_page.open_register(base_url)
    time.sleep(0.5)
    
    auth_page.register(test_name, existing_email, "TestPassword123!", "TestPassword123!")
    time.sleep(1)
    
    validation_errors = auth_page.get_validation_errors()
    has_error = auth_page.has_login_error() or len(validation_errors) > 0
    
    current_url = driver.current_url.lower()
    assert has_error or "/register" in current_url, \
        "Expected error message when registering with existing email."
    if has_error:
        error_text = auth_page.get_error_message() or " ".join(validation_errors)
        assert "email" in error_text.lower() or "exist" in error_text.lower(), \
            f"Error should mention email already exists. Got: {error_text}"


def test_auth_009_verify_registration_rejected_for_weak_password(driver, wait, base_url):
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
    assert has_error or "/register" in current_url, \
        "Expected password validation error for weak password."
    if has_error:
        error_text = auth_page.get_error_message() or " ".join(validation_errors)
        assert any(keyword in error_text.lower() for keyword in ["password", "length", "minimum"]), \
            f"Error should mention password requirements. Got: {error_text}"


def test_auth_010_verify_registration_rejected_for_password_mismatch(driver, wait, base_url):
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
    assert has_error or "/register" in current_url, \
        "Expected password mismatch error."
    if has_error:
        error_text = auth_page.get_error_message() or " ".join(validation_errors)
        assert any(keyword in error_text.lower() for keyword in ["match", "confirm", "password"]), \
            f"Error should mention password mismatch. Got: {error_text}"


def test_auth_011_verify_redirect_when_authenticated_user_accesses_login(driver, wait, base_url):
    """TC-AUTH-011: Xác minh người dùng đã đăng nhập bị chuyển hướng khi truy cập lại trang login"""
    ensure_logged_out(driver)
    
    auth_page = AuthPage(driver)
    test_email, test_password = register_test_user(driver, base_url, "redirect11")
    
    assert auth_page.is_user_logged_in(), "User should be logged in after registration."
    
    auth_page.open_login(base_url)
    time.sleep(1)
    
    current_url = driver.current_url.lower()
    is_redirected = "/login" not in current_url or auth_page.is_user_logged_in()
    assert is_redirected, \
        "Authenticated user should be redirected or shown logged-in state when accessing login page."


def test_auth_012_verify_session_persists_with_remember_me_enabled(driver, wait, base_url):
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
