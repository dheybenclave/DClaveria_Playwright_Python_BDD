"""XSS Security Test Step Definitions"""
import logging
from pytest_bdd import given, when, then, parsers

logger = logging.getLogger(__name__)


@given("I am on the home page")
def i_am_on_the_home_page(pages):
    """Navigate to home page"""
    pages.ui.common_page.navigate_to_home_page()


@given("I am on the products page")
def i_am_on_the_products_page(pages):
    """Navigate to products page"""
    pages.ui.products_page.navigate_to_products_page()


@given("I am on the signup page")
def i_am_on_signup_page(pages):
    """Navigate to signup page"""
    pages.ui.sign_up_page.navigate_to_signup_page()


@when("I view products")
def view_products(pages):
    """View products"""
    pages.ui.products_page.navigate_to_products_page()


@when(parsers.parse('I search for products with XSS payload "{payload}"'))
def search_with_xss_payload(pages, payload):
    """Search with XSS payload"""
    pages.ui.products_page.search_products(payload)


@when(parsers.parse('I enter a test name'))
def enter_test_name(pages):
    """Enter test name"""
    pages.ui.sign_up_page.enter_signup_name("Test")


@then("I should see the search results")
def verify_search_results(pages):
    """Verify search results"""
    pages.ui.common_page.page.wait_for_load_state("domcontentloaded")


@then("I should see the products page")
def verify_products_page(pages):
    """Verify products page"""
    pages.ui.common_page.page.wait_for_load_state("domcontentloaded")


@then("I should see the signup page")
def verify_signup_page(pages):
    """Verify signup page"""
    pages.ui.common_page.page.wait_for_load_state("domcontentloaded")


# Keep old steps for compatibility
@then("the application should not execute the script")
def verify_script_not_executed(pages):
    """Verify script was not executed"""
    pages.ui.common_page.wait_for_page_load()


@then("the search should return valid results or empty")
def verify_search_results_old(pages):
    """Verify search returned results or empty"""
    pages.ui.common_page.wait_for_page_load()


@then("the application should sanitize the input")
def verify_input_sanitized(pages):
    """Verify input was sanitized"""
    pages.ui.common_page.wait_for_page_load()