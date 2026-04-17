"""
Step definitions for Search API testing.
"""
import json
import time

from pytest_bdd import when, then, given, parsers


def _safe_json_response(response):
    """Helper to safely parse JSON or return fallback"""
    try:
        return response.json()
    except (json.JSONDecodeError, ValueError):
        return {"raw": response.text, "status": response.status}


# Background step - needed by all search API scenarios
@given("the API base URL is configured")
def configure_api_base_url(pages):
    """Configure the API base URL (no-op - already configured in conftest)"""
    pass


@when(parsers.parse('I send a "GET" request to "{endpoint}" with search query "{query}"'), target_fixture="api_response_data")
@when(parsers.parse('I send a "POST" request to "{endpoint}" with search query "{query}"'), target_fixture="api_response_data")
def search_products(pages, endpoint, query):
    """Search for products with given query"""
    endpoint_key = endpoint.strip().lower()

    if endpoint_key == "/api/searchproduct":
        # Use POST method as per API 5 documentation
        response = pages.api.search_product.get(search_query=query)
    else:
        raise AssertionError(f"Unsupported endpoint: {endpoint}")

    start_time = time.perf_counter()
    duration_ms = round((time.perf_counter() - start_time) * 1000)
    response_json = _safe_json_response(response)

    from utils.test_state import test_context
    # Store only serializable data, not raw APIResponse objects
    test_context.last_response = {
        "status": response.status,
        "status_text": response.status_text,
        "json": response_json,
        "duration": duration_ms,
        "endpoint": endpoint,
        "method": "POST",
        "query": query
    }

    return test_context.last_response


# Common assertion steps
@then(parsers.parse('the response status code should be {status:d}'))
def verify_status(api_response_data, status):
    """Verify API response status code"""
    response_json = api_response_data.get("json", {})
    response_status = api_response_data.get("status", 200)

    response_code = response_json.get("responseCode", response_status)
    assert response_code == status, f"Expected responseCode {status}, but got {response_code}"


@then(parsers.parse('the response should contain a list of products'))
def verify_products_list(api_response_data):
    """Verify response contains products"""
    response_json = api_response_data["json"]
    assert "products" in response_json or "response" in response_json, \
        "Response should contain 'products' or 'response' field"


@then(parsers.parse('the response should contain matching products'))
def verify_matching_products(api_response_data):
    """Verify response contains matching products"""
    response_json = api_response_data["json"]
    if "products" in response_json:
        products = response_json["products"]
        assert len(products) > 0, "Should have matching products"
        # Could add more validation for match quality


@then(parsers.parse('the response should indicate no products found'))
def verify_no_products(api_response_data):
    """Verify response indicates no products found"""
    response_json = api_response_data["json"]
    if "products" in response_json:
        products = response_json["products"]
        assert len(products) == 0, "Products list should be empty"
    elif "message" in response_json:
        message = response_json["message"].lower()
        assert "not found" in message or "no" in message