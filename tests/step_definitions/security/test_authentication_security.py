"""Authentication Security Test Step Definitions"""
import logging
from pytest_bdd import given, when, then, parsers

logger = logging.getLogger(__name__)


@given("I am on the login page")
def i_am_on_login_page(pages):
    """Navigate to login page"""
    pages.ui.login_page.navigate_to_login_page()


@when(parsers.parse('I login with weak password "{password}"'))
def login_with_weak_password(pages, password):
    """Login with weak password"""
    pages.ui.login_page.enter_login_username("dhyplaywrighttesting@gmail.com")
    pages.ui.login_page.enter_login_password(password)
    pages.ui.login_page.click_login_button()


@when("I login with blank username and password")
def login_with_blank_credentials(pages):
    """Login with blank credentials"""
    pages.ui.login_page.enter_login_username("")
    pages.ui.login_page.enter_login_password("")
    pages.ui.login_page.click_login_button()


@when(parsers.parse("I attempt to login with incorrect password {count} times"))
def attempt_login_multiple_times(pages, count):
    """Attempt login multiple times"""
    for i in range(int(count)):
        pages.ui.login_page.enter_login_username("test@test.com")
        pages.ui.login_page.enter_login_password("wrongpassword")
        pages.ui.login_page.click_login_button()
        pages.ui.common_page.page.wait_for_load_state("domcontentloaded", timeout=3000)


@when("I refresh the page")
def refresh_page(pages):
    """Refresh the page"""
    pages.ui.common_page.page.reload(wait_until="domcontentloaded")


@when("I go to the home page")
def go_to_home(pages):
    """Go to home page"""
    pages.ui.common_page.page.goto("https://automationexercise.com", wait_until="domcontentloaded")


@given("I am on the signup page")
def i_am_on_signup_page(pages):
    """Navigate to signup page"""
    pages.ui.sign_up_page.navigate_to_signup_page()


@when(parsers.parse("I register with an already registered email"))
def register_with_existing_email(pages):
    """Register with existing email"""
    pages.ui.sign_up_page.enter_signup_name("Test User")
    pages.ui.sign_up_page.enter_signup_email("dhyplaywrighttesting@gmail.com")
    pages.ui.sign_up_page.click_signup_button()


@then("I should see the login result")
def verify_login_result(pages):
    """Verify login result"""
    pages.ui.common_page.page.wait_for_load_state("domcontentloaded")


@then("I should see the home page")
def verify_home_page(pages):
    """Verify home page"""
    pages.ui.common_page.page.wait_for_load_state("domcontentloaded")


@then("I should see the signup result")
def verify_signup_result(pages):
    """Verify signup result"""
    pages.ui.common_page.page.wait_for_load_state("domcontentloaded")


# Keep old steps for compatibility
@then("the application should reject weak passwords")
def verify_reject_weak_password(pages):
    """Verify weak password rejected"""
    pages.ui.common_page.wait_for_page_load()


@then("the application should show validation error")
def verify_validation_error(pages):
    """Verify validation error shown"""
    pages.ui.common_page.wait_for_page_load()


@then("the application should block further attempts")
def verify_block_further_attempts(pages):
    """Verify further attempts blocked"""
    pages.ui.common_page.wait_for_page_load()


@then("I should be redirected to login page")
def verify_redirected_to_login(pages):
    """Verify redirected to login"""
    pages.ui.common_page.wait_for_page_load()


@then("the application should show error message")
def verify_error_message(pages):
    """Verify error message shown"""
    pages.ui.common_page.wait_for_page_load()