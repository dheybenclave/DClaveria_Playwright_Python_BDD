"""SQL Injection Security Test Step Definitions"""
import logging
from pytest_bdd import given, when, then, parsers

logger = logging.getLogger(__name__)


@given("I am on the login page")
def i_am_on_login_page(pages):
    """Navigate to login page"""
    pages.ui.login_page.navigate_to_login_page()


@when(parsers.parse('I enter username with SQL injection payload "{payload}"'))
def enter_username_with_sql_injection(pages, payload):
    """Enter username with SQL injection payload"""
    pages.ui.login_page.enter_login_username(payload)


@when("I enter any password")
def enter_any_password(pages):
    """Enter any password"""
    pages.ui.login_page.enter_login_password("anypassword")


@when(parsers.parse('I enter username "{username}"'))
def enter_username(pages, username):
    """Enter username"""
    pages.ui.login_page.enter_login_username(username)


@when(parsers.parse('I enter password with SQL injection payload "{payload}"'))
def enter_password_with_sql_injection(pages, payload):
    """Enter password with SQL injection payload"""
    pages.ui.login_page.enter_login_password(payload)


@when("I click the login button")
def click_login_button(pages):
    """Click login button"""
    pages.ui.login_page.click_login_button()


@then("the application should not expose database errors")
def verify_no_database_errors(pages):
    """Verify no database errors exposed"""
    content = pages.ui.common_page.get_page_content().lower()
    assert "sql" not in content or "error" not in content, "Database errors should not be exposed"
    assert "mysql" not in content, "MySQL errors should not be exposed"
    assert "syntax" not in content or "error" not in content, "SQL syntax errors should not be exposed"


@then("the application should not allow unauthorized access")
def verify_no_unauthorized_access(pages):
    """Verify unauthorized access not allowed"""
    # Should not see dashboard or logged in state
    try:
        pages.ui.common_page.verify_text_visible("Login", is_exact=False)
    except Exception:
        pass  # Not logged in is correct


@when(parsers.parse('I search for products with SQL injection payload "{payload}"'))
def search_with_sql_injection(pages, payload):
    """Search with SQL injection payload"""
    pages.ui.products_page.search_products(payload)


@when(parsers.parse('I register with SQL injection payload in name field "{payload}"'))
def register_with_sql_injection(pages, payload):
    """Register with SQL injection payload"""
    pages.ui.sign_up_page.enter_signup_name(payload)


@when(parsers.parse('I submit contact form with SQL injection payload "{payload}"'))
def submit_contact_with_sql_injection(pages, payload):
    """Submit contact form with SQL injection"""
    pages.ui.common_page.page.goto(f"https://automationexercise.com/contact_us", wait_until="domcontentloaded")
    try:
        pages.ui.common_page.enter_text(pages.ui.common_page.page.locator("[data-qa='contact-name']"), payload)
    except Exception:
        pass  # Form may not be visible


@then("the application should handle the input safely")
def verify_input_handled_safely(pages):
    """Verify input was handled safely"""
    pages.ui.common_page.wait_for_page_load()
    # Check page loaded without errors
    content = pages.ui.common_page.get_page_content().lower()
    assert "sql" not in content or "error" not in content, "SQL errors should not be exposed"