"""
Step definitions for XSS Security Testing.
"""
from pytest_bdd import when, then, given, parsers

from utils.security_payloads import SecurityPayloads, SecurityTestHelpers


# XSS - Search Tests
@when("I search for products with XSS payload {payload}")
def search_with_xss(pages, payload):
    """Search with XSS payload"""
    if payload == "<script>alert('XSS')</script>":
        payload = SecurityPayloads.get_xss_payload(0)
    pages.ui.products_page.enter_search_query(payload)
    pages.ui.products_page.click_search_button()


@then("the application should not execute the script")
def verify_no_script_execution(pages):
    """Verify script is not executed"""
    page_content = pages.ui.common_page.get_page_content()

    # The raw XSS payload should not be present in the page
    # or should be escaped
    assert SecurityTestHelpers.should_not_expose_xss(page_content), \
        "XSS payload was not sanitized!"


@then("the search should return valid results or empty")
def verify_valid_search(pages):
    """Verify search returns valid results"""
    # Just ensure page loaded without JS errors
    assert pages.ui.common_page.is_page_loaded()


# XSS - Contact Form Tests
@when("I submit contact form with XSS payload {payload}")
def submit_contact_with_xss(pages, payload):
    """Submit contact form with XSS payload"""
    if payload == "<img src=x onerror=alert('XSS')>":
        payload = SecurityPayloads.get_xss_payload(3)

    pages.ui.common_page.enter_contact_name("Test User")
    pages.ui.common_page.enter_contact_email("test@test.com")
    pages.ui.common_page.enter_contact_subject(payload)
    pages.ui.common_page.enter_contact_message("Test Message")
    pages.ui.common_page.click_contact_submit_button()


@then("the application should sanitize the input")
def verify_xss_sanitization(pages):
    """Verify XSS is sanitized"""
    page_content = pages.ui.common_page.get_page_content()

    # Check for raw script tags or XSS indicators
    for payload in SecurityPayloads.XSS_PAYLOADS[:3]:
        assert payload not in page_content, \
            f"XSS payload not sanitized: {payload}"


# XSS - Register Tests
@when("I register with XSS payload in name field {payload}")
def register_with_xss(pages, payload):
    """Register with XSS in name field"""
    import uuid
    if payload == "<script>alert('XSS')</script>":
        payload = SecurityPayloads.get_xss_payload(0)

    unique_id = uuid.uuid4().hex[:8]
    pages.ui.sign_up_page.enter_signup_name(payload)
    pages.ui.sign_up_page.enter_signup_email(f"test_{unique_id}@test.com")
    pages.ui.sign_up_page.click_signup_button()


# XSS - Review Tests
@given("I am logged in as a registered user")
def login_as_registered_user(pages):
    """Login as registered user"""
    # This would need user credentials from test data
    pages.ui.login_page.navigate_to_login_page()
    # Login with test user credentials
    pages.ui.login_page.enter_login_username("test@test.com")
    pages.ui.login_page.enter_login_password("TestPassword123!")
    pages.ui.login_page.click_login_button()


@given("I am on a product detail page")
def navigate_to_product_detail(pages):
    """Navigate to product detail page"""
    pages.ui.products_page.navigate_to_products_page()
    # Click on first product
    pages.ui.products_page.click_first_product()


@when("I submit a review with XSS payload {payload}")
def submit_review_with_xss(pages, payload):
    """Submit product review with XSS"""
    if payload == "<svg onload=alert('XSS')>":
        payload = SecurityPayloads.get_xss_payload(4)

    pages.ui.products_page.enter_review_name("Test User")
    pages.ui.products_page.enter_review_message(payload)
    pages.ui.products_page.submit_review()


@then("the review should be stored safely")
def verify_review_stored_safely(pages):
    """Verify review is stored without XSS execution"""
    page_content = pages.ui.common_page.get_page_content()

    # Check page doesn't contain unescaped XSS
    assert SecurityTestHelpers.should_not_expose_xss(page_content)


# Reflected XSS Tests
@when("I search for products with reflected XSS payload {payload}")
def search_with_reflected_xss(pages, payload):
    """Search with reflected XSS payload"""
    if payload == "><script>alert('XSS')</script>":
        payload = SecurityPayloads.get_xss_payload(18)

    pages.ui.products_page.enter_search_query(payload)
    pages.ui.products_page.click_search_button()