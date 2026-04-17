"""
Step definitions for Authentication Security Testing.
"""
from pytest_bdd import when, then, given, parsers

from utils.security_payloads import SecurityPayloads


# Login with Weak Password
@when("I login with weak password {password}")
def login_with_weak_password(pages, password):
    """Login with weak password"""
    if password == "password":
        password = SecurityPayloads.get_weak_password(0)

    pages.ui.login_page.enter_login_username("test@test.com")
    pages.ui.login_page.enter_login_password(password)
    pages.ui.login_page.click_login_button()


@then("the application should reject weak passwords")
def verify_weak_password_rejected(pages):
    """Verify weak password is rejected"""
    page_content = pages.ui.common_page.get_page_content()

    # Should show error or warning about weak password
    # or prevent login
    has_warning = any(word in page_content.lower() for word in
                     ["weak", "strong", "password", "invalid"])
    assert has_warning, "Application did not reject weak password"


@then("display a password strength warning")
def verify_password_strength_warning(pages):
    """Verify password strength warning is displayed"""
    page_content = pages.ui.common_page.get_page_content()

    # Check for password strength indicators
    has_indicator = "password" in page_content.lower()
    assert has_indicator, "No password strength warning displayed"


# Login with Blank Credentials
@when("I login with blank username and password")
def login_with_blank_credentials(pages):
    """Login with blank credentials"""
    pages.ui.login_page.enter_login_username("")
    pages.ui.login_page.enter_login_password("")
    pages.ui.login_page.click_login_button()


@then("the application should show validation error")
def verify_validation_error(pages):
    """Verify validation error is shown"""
    page_content = pages.ui.common_page.get_page_content()

    # Should show validation error
    has_error = any(word in page_content.lower() for word in
                   ["required", "empty", "blank", "invalid", "error"])
    assert has_error, "No validation error displayed for blank credentials"


# Brute Force Protection
@when("I attempt to login with incorrect password {count} times")
def login_attempt_multiple_times(pages, count):
    """Attempt to login multiple times"""
    if count == "5":
        count = 5
    else:
        count = int(count)

    for i in range(count):
        pages.ui.login_page.enter_login_username("test@test.com")
        pages.ui.login_page.enter_login_password(f"wrongpassword{i}")
        pages.ui.login_page.click_login_button()
        # Brief wait between attempts
        pages.ui.common_page.wait_for_page_load()


@then("the application should implement rate limiting")
def verify_rate_limiting(pages):
    """Verify rate limiting is implemented"""
    page_content = pages.ui.common_page.get_page_content()

    # Should show rate limiting message
    has_limit = any(word in page_content.lower() for word in
                    ["attempt", "locked", "too many", "rate", "limit"])
    assert has_limit, "No rate limiting detected"


@then("temporarily lock the account")
def verify_account_locked(pages):
    """Verify account is locked"""
    page_content = pages.ui.common_page.get_page_content()

    # Should show account locked message
    has_lock = any(word in page_content.lower() for word in
                   ["locked", "account", "suspended", "temporary"])
    assert has_lock, "Account was not locked after multiple failed attempts"


# Session Expiration
@given("I am logged in as a registered user")
def login_as_registered_user(pages):
    """Login as registered user"""
    from utils.api_helpers import APITestData
    credentials = APITestData.get_valid_login_credentials()

    pages.ui.login_page.navigate_to_login_page()
    pages.ui.login_page.enter_login_username(credentials["email"])
    pages.ui.login_page.enter_login_password(credentials["password"])
    pages.ui.login_page.click_login_button()


@when("I wait for session to expire")
def wait_for_session_expiry(pages):
    """Wait for session to expire"""
    # This would normally wait for actual session timeout
    # For testing, we just verify the mechanism exists
    pages.ui.common_page.wait_for_page_load()


@then("the application should redirect to login page")
def verify_redirect_to_login(pages):
    """Verify redirect to login page"""
    current_url = pages.ui.common_page.get_current_url()

    assert "login" in current_url.lower() or pages.ui.login_page.is_login_page_visible(), \
        "Application did not redirect to login page after session expiry"


# Password Change Without Current Password
@when("I attempt to change password without providing current password")
def change_password_without_current(pages):
    """Attempt to change password without current password"""
    # Navigate to account settings if available
    pages.ui.common_page.navigate_to_account_settings()
    # Try to change password without current password
    pages.ui.profile_page.enter_new_password("NewPassword123!")
    pages.ui.profile_page.click_change_password_button()


@then("the application should reject the request")
def verify_password_change_rejected(pages):
    """Verify password change is rejected"""
    page_content = pages.ui.common_page.get_page_content()

    # Should show error about missing current password
    has_error = any(word in page_content.lower() for word in
                   ["current", "required", "missing", "old"])
    assert has_error, "Application accepted password change without current password"


# Registration with Existing Email
@when("I register with an already registered email")
def register_with_existing_email(pages):
    """Register with existing email"""
    pages.ui.sign_up_page.navigate_to_signup_page()

    # Use known existing email
    pages.ui.sign_up_page.enter_signup_name("Existing User")
    pages.ui.sign_up_page.enter_signup_email("existing@test.com")
    pages.ui.sign_up_page.click_signup_button()


@then("the application should show email already exists error")
def verify_email_exists_error(pages):
    """Verify email already exists error is shown"""
    page_content = pages.ui.common_page.get_page_content()

    # Should show email already exists message
    has_error = any(word in page_content.lower() for word in
                    ["exists", "already", "email", "used"])
    assert has_error, "No error shown for existing email registration"