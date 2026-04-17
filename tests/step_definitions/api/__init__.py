"""
Common step definitions for all API test suites.
"""
from pytest_bdd import given


@given("the API base URL is configured")
def configure_api_base_url(pages):
    """Verify the API base URL is configured (no-op - already configured via conftest)"""
    # The API base URL is already configured in conftest.py via request_context
    # This step exists for clarity in BDD scenarios but requires no action
    pass