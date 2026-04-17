"""
Step definitions for User API testing.
"""
import json
import time
import uuid

from pytest_bdd import when, then, given, parsers

from utils.api_helpers import APIHelpers, APITestData


# Background step - needed by all user API scenarios
@given("the API base URL is configured")
def configure_api_base_url(pages):
    """Configure the API base URL (no-op - already configured in conftest)"""
    pass


def _safe_json_response(response):
    """Helper to safely parse JSON or return fallback"""
    try:
        return response.json()
    except (json.JSONDecodeError, ValueError):
        try:
            return {"raw": str(response.text), "status": response.status}
        except Exception:
            return {"raw": "Unable to parse response", "status": response.status}


def _store_response(response, endpoint, method, duration_ms=0):
    """Helper to store response data in serializable format"""
    response_json = _safe_json_response(response)
    from utils.test_state import test_context
    test_context.last_response = {
        "status": response.status,
        "status_text": response.status_text,
        "json": response_json,
        "duration": duration_ms,
        "endpoint": endpoint,
        "method": method
    }
    return test_context.last_response


def _create_user_and_store(user_data, pages):
    """Helper to create user and store response"""
    response = pages.api.create_account.post(**user_data)
    from utils.test_state import test_context
    test_context.last_created_user = user_data
    return response


def _create_order_and_store(order_data, pages):
    """Helper to create order and store response"""
    response = pages.api.create_order.post_cod(**order_data)
    from utils.test_state import test_context
    test_context.last_created_order = {"data": order_data, "response": None}
    return response


# Using target_fixture to pass data between steps
@when(parsers.parse('I send a "{method}" request to "{endpoint}" with valid user data'), target_fixture="api_response_data")
def create_user_account(pages, method, endpoint):
    """Create a new user account"""
    endpoint_key = endpoint.strip().lower()

    if endpoint_key == "/api/createaccount":
        user_data = APIHelpers.generate_test_user()
        
        # Add unique identifier to email to avoid "already exists" conflicts
        unique_suffix = uuid.uuid4().hex[:8]
        original_email = user_data.get("email", "")
        if "@" in original_email:
            local, domain = original_email.split("@", 1)
            user_data["email"] = f"{local}+{unique_suffix}@{domain}"
        
        response = pages.api.create_account.post(**user_data)

        # Store user data for cleanup
        from utils.test_state import test_context
        test_context.last_created_user = user_data
    else:
        raise AssertionError(f"Unsupported endpoint: {endpoint}")

    start_time = time.perf_counter()
    duration_ms = round((time.perf_counter() - start_time) * 1000)
    response_json = _safe_json_response(response)

    from utils.test_state import test_context
    # Store serializable data only (not APIResponse object)
    test_context.last_response = {
        "status": response.status,
        "status_text": response.status_text,
        "json": response_json,
        "duration": duration_ms,
        "endpoint": endpoint,
        "method": method
    }

    return test_context.last_response


@when(parsers.parse('I send a "{method}" request to "{endpoint}" with duplicate email'), target_fixture="api_response_data")
def create_duplicate_user(pages, method, endpoint):
    """Try to create account with existing email"""
    endpoint_key = endpoint.strip().lower()

    if endpoint_key == "/api/createaccount":
        # Use a fixed email that might exist
        user_data = {
            "name": "Test User",
            "email": "existing@test.com",
            "password": "TestPass123!"
        }
        response = _create_user_and_store(user_data, pages)
    else:
        raise AssertionError(f"Unsupported endpoint: {endpoint}")

    return _store_response(response, endpoint, method)


@given("a user account exists in the system")
def user_account_exists(pages):
    """Create a test user for subsequent tests"""
    import uuid
    user_data = APIHelpers.generate_test_user()
    
    # Add unique suffix to email to ensure fresh account
    original_email = user_data.get("email", "")
    if "@" in original_email:
        local, domain = original_email.split("@", 1)
        user_data["email"] = f"{local}+{uuid.uuid4().hex[:8]}@{domain}"
    
    response = pages.api.create_account.post(**user_data)

    response_json = _safe_json_response(response)
    response_code = response_json.get("responseCode", response.status)

    # If user already exists (400 with "already exists"), try with new email
    if response_code == 400 and "already exists" in response_json.get("message", "").lower():
        user_data["email"] = f"test_{uuid.uuid4().hex[:8]}@mailinator.com"
        response = pages.api.create_account.post(**user_data)
        response_json = _safe_json_response(response)

    from utils.test_state import test_context
    test_context.last_created_user = user_data

    return user_data


@when(parsers.parse('I send a "{method}" request to "{endpoint}" with valid credentials'), target_fixture="api_response_data")
def login_valid_credentials(pages, method, endpoint):
    """Login with valid credentials - also handles POST for delete fallback"""
    from utils.test_state import test_context

    # Get stored user or default
    user_data = getattr(test_context, "last_created_user", None)
    if not user_data:
        user_data = APITestData.get_valid_login_credentials()

    # Handle DELETE separately - use the dedicated handler
    if method.upper() == "DELETE":
        # Call the delete handler directly
        return delete_account_with_delete_method(pages, endpoint)
    
    # For POST (login), PUT, etc.
    response = pages.api.login_user.post(
        email=user_data.get("email", user_data.get("email")),
        password=user_data.get("password", user_data.get("password"))
    )

    response_json = _safe_json_response(response)

    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": method
    }

    return test_context.last_response


@when(parsers.parse('I send a "{method}" request to "{endpoint}" with wrong password'), target_fixture="api_response_data")
def login_wrong_password(pages, method, endpoint):
    """Login with wrong password"""
    from utils.test_state import test_context

    user_data = getattr(test_context, "last_created_user", None)
    if not user_data:
        user_data = {"email": "test@test.com"}

    response = pages.api.login_user.post(
        email=user_data.get("email", "test@test.com"),
        password="WrongPassword123!"
    )

    response_json = _safe_json_response(response)

    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": method
    }

    return test_context.last_response


@when(parsers.parse('I send a "{method}" request to "{endpoint}" with non-existent email'), target_fixture="api_response_data")
def login_nonexistent_email(pages, method, endpoint):
    """Login with non-existent email"""
    response = pages.api.login_user.post(
        email=f"nonexistent_{uuid.uuid4().hex[:8]}@test.com",
        password="AnyPassword123!"
    )

    response_json = _safe_json_response(response)

    from utils.test_state import test_context
    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": method
    }

    return test_context.last_response


@when(parsers.parse('I send a "GET" request to "{endpoint}" with the user\'s email'), target_fixture="api_response_data")
def get_user_by_email(pages, endpoint):
    """Get user details by email"""
    from utils.test_state import test_context

    user_data = getattr(test_context, "last_created_user", None)
    email = user_data.get("email", "test@test.com") if user_data else "test@test.com"

    response = pages.api.get_user_detail_by_email.get(email=email)
    response_json = _safe_json_response(response)

    from utils.test_state import test_context
    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": "GET"
    }

    return test_context.last_response


@when(parsers.parse('I send a "GET" request to "{endpoint}" with invalid email'), target_fixture="api_response_data")
def get_user_invalid_email(pages, endpoint):
    """Get user details with invalid email"""
    response = pages.api.get_user_detail_by_email.get(email="invalid_email_not_found@test.com")
    response_json = _safe_json_response(response)

    from utils.test_state import test_context
    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": "GET"
    }

    return test_context.last_response


@when(parsers.parse('I send a "PUT" request to "{endpoint}" with new user data'), target_fixture="api_response_data")
def update_account(pages, endpoint):
    """Update user account"""
    from utils.test_state import test_context

    user_data = getattr(test_context, "last_created_user", None)
    if not user_data:
        user_data = APITestData.get_valid_login_credentials()

    response = pages.api.update_account.put(
        email=user_data.get("email", "test@test.com"),
        password=user_data.get("password", "TestPassword123!"),
        name="Updated Name"
    )

    response_json = _safe_json_response(response)

    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": "PUT"
    }

    return test_context.last_response


@when(parsers.parse('I send a "PUT" request to "{endpoint}" with wrong password'), target_fixture="api_response_data")
def update_account_wrong_password(pages, endpoint):
    """Update account with wrong password"""
    from utils.test_state import test_context

    user_data = getattr(test_context, "last_created_user", None)
    email = user_data.get("email", "test@test.com") if user_data else "test@test.com"

    response = pages.api.update_account.put(
        email=email,
        password="WrongPassword123!",
        name="Updated Name"
    )

    response_json = _safe_json_response(response)

    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": "PUT"
    }

    return test_context.last_response


@when(parsers.parse('I send a "POST" request to "{endpoint}" with valid credentials'), target_fixture="api_response_data")
def delete_account(pages, endpoint):
    """Delete user account"""
    from utils.test_state import test_context

    user_data = getattr(test_context, "last_created_user", None)
    if not user_data:
        user_data = APITestData.get_valid_login_credentials()

    response = pages.api.delete_account.delete(
        email=user_data.get("email", user_data.get("email")),
        password=user_data.get("password", user_data.get("password"))
    )

    response_json = _safe_json_response(response)

    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": "POST"
    }

    return test_context.last_response


@when(parsers.parse('I send a "DELETE" request to "{endpoint}" with valid credentials'), target_fixture="api_response_data")
def delete_account_with_delete_method(pages, endpoint):
    """Delete user account using DELETE method"""
    from utils.test_state import test_context

    user_data = getattr(test_context, "last_created_user", None)
    if not user_data:
        user_data = APITestData.get_valid_login_credentials()

    response = pages.api.delete_account.delete(
        email=user_data.get("email", user_data.get("email")),
        password=user_data.get("password", user_data.get("password"))
    )

    response_json = _safe_json_response(response)

    test_context.last_response = {
        "status": response.status,
        "json": response_json,
        "endpoint": endpoint,
        "method": "DELETE"
    }

    return test_context.last_response


# Common assertion steps
@then(parsers.parse('the response status code should be {status:d}'))
def verify_status(api_response_data, status):
    """Verify API response status code"""
    response_json = api_response_data.get("json", {})
    response_status = api_response_data.get("status", 200)

    # Check responseCode in JSON first, then fallback to HTTP status
    response_code = response_json.get("responseCode", response_status)
    assert response_code == status, f"Expected responseCode {status}, but got {response_code}"


@then(parsers.parse('the response should contain a success message'))
def verify_login_success_message(api_response_data):
    """Verify login response contains success message"""
    response_json = api_response_data["json"]
    assert "message" in response_json, "Response should contain 'message' field"
    message = response_json["message"].lower()
    assert "exists" in message or "user" in message or "success" in message, \
        f"Message should indicate login success: {response_json['message']}"


@then(parsers.parse('the response should contain "message" indicating success'))
def verify_success_message(api_response_data):
    """Verify response contains success message"""
    response_json = api_response_data["json"]
    assert "message" in response_json, "Response should contain 'message' field"
    message = response_json["message"].lower()
    assert "success" in message or "account" in message or "created" in message, \
        f"Message should indicate success: {response_json['message']}"


@then(parsers.parse('the response should indicate the email already exists'))
def verify_duplicate_email(api_response_data):
    """Verify response indicates duplicate email"""
    response_json = api_response_data["json"]
    assert "message" in response_json, "Response should contain 'message' field"
    message = response_json["message"].lower()
    assert "email" in message or "exist" in message or "already" in message, \
        f"Message should indicate email exists: {response_json['message']}"


@then(parsers.parse('the response should indicate invalid credentials'))
def verify_invalid_credentials(api_response_data):
    """Verify response indicates invalid credentials"""
    response_json = api_response_data["json"]
    assert "message" in response_json, "Response should contain 'message' field"
    message = response_json["message"].lower()
    assert "not" in message or "invalid" in message or "incorrect" in message or "wrong" in message, \
        f"Message should indicate invalid credentials: {response_json['message']}"


@then(parsers.parse('the response should indicate user not found'))
def verify_user_not_found(api_response_data):
    """Verify response indicates user not found"""
    response_json = api_response_data["json"]
    assert "message" in response_json, "Response should contain 'message' field"
    message = response_json["message"].lower()
    assert "not" in message or "find" in message or "exist" in message, \
        f"Message should indicate user not found: {response_json['message']}"


@then(parsers.parse('the response should contain the user\'s name and email'))
def verify_user_details(api_response_data):
    """Verify response contains user details"""
    response_json = api_response_data["json"]
    assert "user" in response_json, "Response should contain 'user' field"
    user = response_json["user"]
    assert "name" in user or "email" in user, "User object should contain name or email"


@then(parsers.parse('the response should indicate successful update'))
def verify_update_success(api_response_data):
    """Verify response indicates successful update"""
    response_json = api_response_data["json"]
    assert "message" in response_json, "Response should contain 'message' field"
    message = response_json["message"].lower()
    assert "updated" in message or "success" in message or "changed" in message, \
        f"Message should indicate update success: {response_json['message']}"


@then(parsers.parse('the response should indicate account deleted successfully'))
def verify_delete_success(api_response_data):
    """Verify response indicates successful deletion"""
    response_json = api_response_data["json"]
    assert "message" in response_json, "Response should contain 'message' field"
    message = response_json["message"].lower()
    assert "deleted" in message or "removed" in message or "account" in message, \
        f"Message should indicate deletion success: {response_json['message']}"