"""
Step definitions for SQL Injection Security Testing.
"""
from pytest_bdd import when, then, given, parsers

from utils.security_payloads import SecurityPayloads, SecurityTestHelpers


# SQL Injection - Login Form Tests
@given("I am on the login page")
def navigate_to_login(pages):
    """Navigate to login page"""
    pages.ui.login_page.navigate_to_login_page()


@when("I enter username with SQL injection payload")
def enter_sql_injection_username(pages):
    """Enter SQL injection payload in username field"""
    payload = SecurityPayloads.get_sql_payload(0)
    pages.ui.login_page.enter_login_username(payload)


@when("I enter any password")
def enter_any_password(pages):
    """Enter any password"""
    pages.ui.login_page.enter_login_password("anypassword")


@when("I enter password with SQL injection payload")
def enter_sql_injection_password(pages):
    """Enter SQL injection payload in password field"""
    payload = SecurityPayloads.get_sql_payload(0)
    pages.ui.login_page.enter_login_password(payload)


@when("I click the login button")
def click_login_button(pages):
    """Click login button"""
    pages.ui.login_page.click_login_button()


@then("the application should not expose database errors")
def verify_no_sql_errors(pages):
    """Verify no SQL errors are exposed"""
    page_content = pages.ui.common_page.get_page_content()

    # Check that SQL error messages are not exposed
    assert SecurityTestHelpers.should_not_expose_sql_errors(page_content), \
        "Application exposed SQL error messages!"


@then("the application should not allow unauthorized access")
def verify_no_unauthorized_access(pages):
    """Verify unauthorized access is not allowed"""
    # If login succeeded with SQL injection, that's a vulnerability
    # Check if we're still on login page or got logged in
    current_url = pages.ui.common_page.get_current_url()
    assert "login" in current_url.lower() or "account" in current_url.lower(), \
        "SQL injection may have allowed unauthorized access!"


# SQL Injection - Search Tests
@given("I am on the products page")
def navigate_to_products(pages):
    """Navigate to products page"""
    pages.ui.products_page.navigate_to_products_page()


@when("I search for products with SQL injection payload {payload}")
def search_with_sql_injection(pages, payload):
    """Search with SQL injection payload"""
    if payload == "' UNION SELECT NULL--":
        payload = SecurityPayloads.get_sql_payload(22)
    pages.ui.products_page.enter_search_query(payload)
    pages.ui.products_page.click_search_button()


@then("the application should display valid search results")
def verify_valid_search_results(pages):
    """Verify valid search results are displayed"""
    # Check that we got valid results or empty response
    # without exposing errors
    page_content = pages.ui.common_page.get_page_content()
    assert SecurityTestHelpers.should_not_expose_sql_errors(page_content)


# SQL Injection - Register Tests
@given("I am on the signup page")
def navigate_to_signup(pages):
    """Navigate to signup page"""
    pages.ui.sign_up_page.navigate_to_signup_page()


@when("I register with SQL injection payload in name field")
def register_with_sql_injection_name(pages):
    """Register with SQL injection in name field"""
    import uuid
    payload = SecurityPayloads.get_sql_payload(0)
    unique_id = uuid.uuid4().hex[:8]

    pages.ui.sign_up_page.enter_signup_name(payload)
    pages.ui.sign_up_page.enter_signup_email(f"test_{unique_id}@test.com")
    pages.ui.sign_up_page.click_signup_button()


@then("the application should handle the input safely")
def verify_safe_input_handling(pages):
    """Verify input is handled safely"""
    page_content = pages.ui.common_page.get_page_content()

    # Should not expose SQL errors
    assert SecurityTestHelpers.should_not_expose_sql_errors(page_content), \
        "Application did not handle SQL injection safely!"


# SQL Injection - Contact Form Tests
@given("I am on the contact us page")
def navigate_to_contact(pages):
    """Navigate to contact us page"""
    pages.ui.common_page.navigate_to_contact_us_page()


@when("I submit contact form with SQL injection payload")
def submit_contact_with_sql_injection(pages):
    """Submit contact form with SQL injection"""
    payload = SecurityPayloads.get_sql_payload(0)

    pages.ui.common_page.enter_contact_name(payload)
    pages.ui.common_page.enter_contact_email("test@test.com")
    pages.ui.common_page.enter_contact_subject("Test Subject")
    pages.ui.common_page.enter_contact_message("Test Message")
    pages.ui.common_page.click_contact_submit_button()


@then("the application should sanitize the input")
def verify_input_sanitization(pages):
    """Verify input is sanitized"""
    page_content = pages.ui.common_page.get_page_content()

    # The payload should not be executed as SQL
    assert SecurityTestHelpers.should_not_expose_sql_errors(page_content)