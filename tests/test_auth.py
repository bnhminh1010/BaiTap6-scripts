import os

import pytest

from pages.auth_page import AuthPage


def _todo():
    pytest.skip("TODO: implement test steps and assertions")


def test_auth_001_verify_login_success_with_valid_credentials(driver, wait, base_url):
    auth_page = AuthPage(driver)
    auth_page.open_login(base_url)

    assert auth_page.is_login_form_displayed(), "Login form is not displayed."

    # Use env vars if provided, otherwise use the default account from assignment doc.
    valid_email = os.getenv("E2E_VALID_EMAIL", "demouser@microsoft.com")
    valid_password = os.getenv("E2E_VALID_PASSWORD", "Password123!")

    auth_page.login(valid_email, valid_password)

    wait.until(lambda d: "/login" not in d.current_url.lower())
    assert not auth_page.is_on_login_page(), "User should be redirected after successful login."


def test_auth_002_verify_login_rejected_with_invalid_password(driver, wait, base_url):
    auth_page = AuthPage(driver)
    auth_page.open_login(base_url)

    assert auth_page.is_login_form_displayed(), "Login form is not displayed."

    auth_page.login("demouser@microsoft.com", "WrongPassword123")
    wait.until(lambda d: auth_page.has_login_error() or auth_page.is_on_login_page())

    assert auth_page.has_login_error(), "Expected login error is not displayed."
    assert auth_page.is_on_login_page(), "User should remain on login page."


def test_auth_003_verify_login_rejected_with_unregistered_email():
    _todo()


def test_auth_004_verify_validation_for_empty_email_and_password():
    _todo()


def test_auth_005_verify_validation_for_invalid_email_format():
    _todo()


def test_auth_006_verify_logout_ends_authenticated_session():
    _todo()


def test_auth_007_verify_registration_success_with_valid_data():
    _todo()


def test_auth_008_verify_registration_rejected_for_existing_email():
    _todo()


def test_auth_009_verify_registration_rejected_for_weak_password():
    _todo()


def test_auth_010_verify_registration_rejected_for_password_mismatch():
    _todo()


def test_auth_011_verify_redirect_when_authenticated_user_accesses_login():
    _todo()


def test_auth_012_verify_session_persists_with_remember_me_enabled():
    _todo()
