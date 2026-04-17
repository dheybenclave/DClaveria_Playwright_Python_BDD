"""
Step definitions for Order API testing.
"""
import json
import time
import uuid

from pytest_bdd import when, then, given, parsers


# Background step - needed by all order API scenarios
@given("the API base URL is configured")
def configure_api_base_url(pages):
    """Configure the API base URL (no-op - already configured in conftest)"""
    pass


@given("an order exists in the system")
def order_exists(pages):
    """Create a test order for subsequent tests"""
    order_data = {
        "name": "Test Customer",
        "email": "test@example.com",
        "phone": "+1234567890",
        "address": "123 Test Street",
        "city": "Test City",
        "state": "Test State",
        "country": "United States",
        "zipcode": "12345"
    }

    response = pages.api.create_order.post_cod(**order_data)
    
    # Handle empty response
    try:
        response_json = response.json()
    except (json.JSONDecodeError, ValueError):
        response_json = {"raw": response.text, "status": response.status}

    from utils.test_state import test_context
    test_context.last_created_order = {
        "data": order_data,
        "response": response_json
    }

    return order_data


@when(parsers.parse('I send a "POST" request to "{endpoint}" with order details'), target_fixture="api_response_data")
def create_order(pages, endpoint):
    """Create a new order"""
    endpoint_key = endpoint.strip().lower()

    if endpoint_key == "/api/createorder":
        order_data = {
            "name": f"Customer_{uuid.uuid4().hex[:6]}",
            "email": f"order_{uuid.uuid4().hex[:8]}@test.com",
            "phone": "+1234567890",
            "address": "123 Test Street",
            "city": "Test City",
            "state": "Test State",
            "country": "United States",
            "zipcode": "12345"
        }
        response = pages.api.create_order.post_cod(**order_data)
    else:
        raise AssertionError(f"Unsupported endpoint: {endpoint}")

    start_time = time.perf_counter()
    duration_ms = round((time.perf_counter() - start_time) * 1000)

    # Handle empty response
    try:
        response_json = response.json()
    except (json.JSONDecodeError, ValueError):
        response_json = {"raw": response.text, "status": response.status}

    from utils.test_state import test_context
    test_context.last_response = {
        "response": response,
        "json": response_json,
        "duration": duration_ms,
        "endpoint": endpoint,
        "method": "POST"
    }
    test_context.last_created_order = {"data": order_data, "response": response_json}

    return test_context.last_response


@when(parsers.parse('I send a "POST" request to "{endpoint}" with missing required fields'), target_fixture="api_response_data")
def create_order_missing_fields(pages, endpoint):
    """Try to create order with missing required fields"""
    endpoint_key = endpoint.strip().lower()

    if endpoint_key == "/api/createorder":
        # Missing required fields - pass empty values
        order_data = {
            "name": "Test Customer",
            "email": "",  # Missing
            "phone": "",  # Missing
            "address": "",  # Missing
            "city": "",  # Missing
            "state": "",  # Missing
            "country": "",  # Missing
            "zipcode": ""  # Missing
        }
        response = pages.api.create_order.post(**order_data)
    else:
        raise AssertionError(f"Unsupported endpoint: {endpoint}")

    # Handle empty response
    try:
        response_json = response.json()
    except (json.JSONDecodeError, ValueError):
        response_json = {"raw": response.text, "status": response.status}

    from utils.test_state import test_context
    test_context.last_response = {
        "response": response,
        "json": response_json,
        "endpoint": endpoint,
        "method": "POST"
    }

    return test_context.last_response


@when(parsers.parse('I send a "GET" request to "{endpoint}" with the order ID'), target_fixture="api_response_data")
def get_order_by_id(pages, endpoint):
    """Get order by order ID"""
    from utils.test_state import test_context

    # Try to get order ID from previous response
    order_response = getattr(test_context, "last_created_order", None)
    order_id = "12345"  # Default fallback

    if order_response:
        response_json = order_response.get("response", {})
        if "orderId" in response_json:
            order_id = response_json["orderId"]
        elif "data" in response_json and "order_id" in response_json["data"]:
            order_id = response_json["data"]["order_id"]

    response = pages.api.get_order_by_order_id.get(order_id=order_id)

    # Handle empty response
    try:
        response_json = response.json()
    except (json.JSONDecodeError, ValueError):
        response_json = {"raw": response.text, "status": response.status}

    test_context.last_response = {
        "response": response,
        "json": response_json,
        "endpoint": endpoint,
        "method": "GET"
    }

    return test_context.last_response


@when(parsers.parse('I send a "GET" request to "{endpoint}" with invalid ID'), target_fixture="api_response_data")
def get_order_invalid_id(pages, endpoint):
    """Get order with invalid ID"""
    response = pages.api.get_order_by_order_id.get(order_id="INVALID_ID_999999")

    # Handle empty response
    try:
        response_json = response.json()
    except (json.JSONDecodeError, ValueError):
        response_json = {"raw": response.text, "status": response.status}

    from utils.test_state import test_context
    test_context.last_response = {
        "response": response,
        "json": response_json,
        "endpoint": endpoint,
        "method": "GET"
    }

    return test_context.last_response


@when(parsers.parse('I send a "GET" request to "{endpoint}"'), target_fixture="api_response_data")
def get_all_orders(pages, endpoint):
    """Get all orders"""
    response = pages.api.get_orders.get()

    # Handle empty response
    try:
        response_json = response.json()
    except (json.JSONDecodeError, ValueError):
        response_json = {"raw": response.text, "status": response.status}

    from utils.test_state import test_context
    test_context.last_response = {
        "response": response,
        "json": response_json,
        "endpoint": endpoint,
        "method": "GET"
    }

    return test_context.last_response


# Common assertion steps
@then(parsers.parse('the response status code should be {status:d}'))
def verify_status(api_response_data, status):
    """Verify API response status code"""
    response_json = api_response_data["json"]
    response = api_response_data["response"]

    response_code = response_json.get("responseCode", response.status)
    assert response_code == status, f"Expected responseCode {status}, but got {response_code}"


@then(parsers.parse('the response should contain "message" indicating order created'))
def verify_order_created(api_response_data):
    """Verify response indicates order created"""
    response_json = api_response_data["json"]
    assert "message" in response_json, "Response should contain 'message' field"
    message = response_json["message"].lower()
    assert "order" in message or "created" in message or "success" in message, \
        f"Message should indicate order created: {response_json['message']}"


@then(parsers.parse('the response should contain an error message'))
def verify_error_message(api_response_data):
    """Verify response contains an error message"""
    response_json = api_response_data["json"]
    assert "message" in response_json or "error" in response_json, \
        "Response should contain an error message"


@then(parsers.parse('the response should contain order details'))
def verify_order_details(api_response_data):
    """Verify response contains order details"""
    response_json = api_response_data["json"]
    # Check for order data in various possible formats
    has_order = ("order" in response_json or "data" in response_json or
                 "orders" in response_json or "orderId" in response_json)
    assert has_order, "Response should contain order details"


@then(parsers.parse('the response should indicate no products found'))
def verify_no_products(api_response_data):
    """Verify response indicates no products found"""
    response_json = api_response_data["json"]
    # API might return empty products array or specific message
    if "products" in response_json:
        assert len(response_json["products"]) == 0, "Products list should be empty"
    elif "message" in response_json:
        message = response_json["message"].lower()
        assert "not found" in message or "no" in message or "empty" in message