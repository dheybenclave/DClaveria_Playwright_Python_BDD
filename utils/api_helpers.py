"""
API Test Helpers Utility

Provides common helper functions for API testing including
authentication, user data management, and request handling.
"""
import os
import json
import random
import string
from typing import Dict, Optional, Any, List


class TestDataManager:
    """Manages test data from JSON files"""

    _test_users: List[Dict[str, Any]] = []
    _current_index = 0
    _initialized = False

    @classmethod
    def _load_test_data(cls) -> List[Dict[str, Any]]:
        """Load test data from JSON file"""
        test_data_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "tests", "test_datas", "json", "register_user_data.json"
        )
        try:
            with open(test_data_file, 'r') as f:
                data = json.load(f)
                # Filter out invalid data entries
                return [user for user in data if user.get("email") and "@" in user.get("email", "")]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load test data: {e}")
            return []

    @classmethod
    def initialize(cls):
        """Initialize test data (call once at start of test run)"""
        if not cls._initialized:
            cls._test_users = cls._load_test_data()
            cls._current_index = 0
            cls._initialized = True

    @classmethod
    def get_next_user(cls) -> Dict[str, Any]:
        """Get next user from test data, cycling through available users"""
        if not cls._initialized:
            cls.initialize()

        if not cls._test_users:
            raise ValueError("No test users available in register_user_data.json")

        user = cls._test_users[cls._current_index].copy()
        cls._current_index = (cls._current_index + 1) % len(cls._test_users)
        
        # Filter to only include fields expected by the API
        return cls._filter_api_fields(user)

    @classmethod
    def _filter_api_fields(cls, user: Dict[str, Any]) -> Dict[str, Any]:
        """Filter user data to only include API-expected fields"""
        # Map JSON fields to API fields (matching CreateAccount.post() parameter names)
        field_mapping = {
            "title": "title",
            "name": "name",
            "email": "email",
            "password": "password",
            "birth_date": "birth_day",
            "birth_month": "birth_month",
            "birth_year": "birth_year",
            "firstname": "firstname",
            "lastname": "lastname",
            "company": "company",
            "address1": "address1",
            "address2": "address2",
            "country": "country",
            "zipcode": "zipcode",
            "state": "state",
            "city": "city",
            "mobile_number": "mobile_number"
        }
        
        required_fields = {"name", "email", "password", "firstname", "lastname", "address1", "city", "state", "zipcode", "mobile_number", "country"}
        
        filtered = {}
        for json_field, api_field in field_mapping.items():
            # Always include field if it exists in source, even if empty
            if json_field in user:
                filtered[api_field] = user[json_field] if user[json_field] else ""
        
        # Ensure all required fields are present (API requires them)
        for field in required_fields:
            if field not in filtered or not filtered[field]:
                filtered[field] = ""
        
        return filtered

    @classmethod
    def get_user_by_id(cls, user_id: str) -> Optional[Dict[str, Any]]:
        """Get specific user by ID"""
        if not cls._initialized:
            cls.initialize()

        for user in cls._test_users:
            if user.get("id") == user_id:
                return user.copy()
        return None

    @classmethod
    def get_user_by_name(cls, name: str) -> Optional[Dict[str, Any]]:
        """Get specific user by name"""
        if not cls._initialized:
            cls.initialize()

        for user in cls._test_users:
            if user.get("name") == name:
                return user.copy()
        return None

    @classmethod
    def reset(cls):
        """Reset to first user (call between tests if needed)"""
        cls._current_index = 0

    @classmethod
    def get_all_users(cls) -> List[Dict[str, Any]]:
        """Get all available test users"""
        if not cls._initialized:
            cls.initialize()
        return cls._test_users.copy()


class APIHelpers:
    """Helper methods for API testing"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")
    API_BASE_URL = f"{BASE_URL}/api"

    @staticmethod
    def generate_random_email(domain: str = "test.com") -> str:
        """Generate a random email address"""
        import random
        import string
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@{domain}"

    @staticmethod
    def generate_random_username() -> str:
        """Generate a random username"""
        import random
        import string
        return f"user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=8))}"

    @staticmethod
    def generate_random_password(length: int = 10) -> str:
        """Generate a random password"""
        import random
        import string
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def generate_test_user() -> Dict[str, str]:
        """Get test user data from JSON file"""
        return TestDataManager.get_next_user()

    @staticmethod
    def build_query_params(params: Dict[str, Any]) -> str:
        """Build URL query string from dictionary"""
        return "&".join([f"{k}={v}" for k, v in params.items() if v is not None])

    @staticmethod
    def validate_response_structure(response_data: dict, expected_keys: list) -> bool:
        """Validate that response contains expected keys"""
        return all(key in response_data for key in expected_keys)

    @staticmethod
    def is_success_response(response_data: dict) -> bool:
        """Check if API response indicates success"""
        if "responseCode" in response_data:
            return response_data["responseCode"] == 200
        if "result" in response_data:
            return response_data["result"] == "ok"
        return response_data.get("success", False)


class APIEndpoints:
    """API endpoint URLs for automationexercise.com"""

    # User API Endpoints
    CREATE_ACCOUNT = "/api/createAccount"
    LOGIN_USER = "/api/loginUser"
    GET_USER_DETAIL_BY_EMAIL = "/api/getUserDetailByEmail"
    UPDATE_ACCOUNT = "/api/updateAccount"
    DELETE_ACCOUNT = "/api/deleteAccount"

    # Product API Endpoints
    PRODUCTS_LIST = "/api/productsList"
    SEARCH_PRODUCT = "/api/searchProduct"

    # Brand API Endpoints
    BRANDS_LIST = "/api/brandsList"

    # Order API Endpoints
    CREATE_ORDER = "/api/createOrder"
    GET_ORDER_BY_ORDER_ID = "/api/getOrderByOrderId"
    GET_ORDERS = "/api/getOrders"

    # Contact API Endpoints
    CONTACT_US = "/api/contactUs"

    @classmethod
    def get_full_url(cls, endpoint: str) -> str:
        """Get full URL for an endpoint"""
        return f"{APIHelpers.API_BASE_URL}{endpoint}"


class APIAssertions:
    """Common API response assertions"""

    @staticmethod
    def assert_response_code(response_data: dict, expected_code: int):
        """Assert response code matches expected"""
        actual_code = response_data.get("responseCode") or response_data.get("code")
        assert actual_code == expected_code, \
            f"Expected response code {expected_code}, got {actual_code}"

    @staticmethod
    def assert_success(response_data: dict):
        """Assert response indicates success"""
        assert APIHelpers.is_success_response(response_data), \
            f"Expected success response, got: {response_data}"

    @staticmethod
    def assert_message(response_data: dict, expected_message: str):
        """Assert response message matches expected"""
        actual_message = response_data.get("message", "")
        assert expected_message.lower() in actual_message.lower(), \
            f"Expected message containing '{expected_message}', got: '{actual_message}'"

    @staticmethod
    def assert_has_message(response_data: dict):
        """Assert response has a message field"""
        assert "message" in response_data, \
            f"Expected 'message' in response, got: {response_data}"

    @staticmethod
    def assert_has_data(response_data: dict):
        """Assert response has data field"""
        assert "data" in response_data or "user" in response_data, \
            f"Expected 'data' or 'user' in response, got: {response_data}"


class APITestData:
    """Test data management for API tests"""

    _test_users = []

    @classmethod
    def create_test_user(cls, page) -> Dict[str, str]:
        """Create a test user via API and store for cleanup"""
        user_data = APIHelpers.generate_test_user()

        # Make API call to create user
        response = page.request.post(
            APIEndpoints.get_full_url(APIEndpoints.CREATE_ACCOUNT),
            data=user_data
        )

        if response.ok:
            cls._test_users.append(user_data)

        return user_data

    @classmethod
    def cleanup_test_users(cls, page):
        """Delete test users created during test run"""
        for user in cls._test_users:
            try:
                page.request.post(
                    APIEndpoints.get_full_url(APIEndpoints.DELETE_ACCOUNT),
                    data={"email": user["email"], "password": user["password"]}
                )
            except Exception:
                pass  # Best effort cleanup

        cls._test_users.clear()

    @classmethod
    def get_valid_login_credentials(cls) -> Dict[str, str]:
        """Get valid credentials for login tests"""
        # Read from test data file or use environment
        test_data_file = "tests/test_datas/json/register_user_data.json"
        try:
            with open(test_data_file, 'r') as f:
                users = json.load(f)
                if users:
                    user = users[0]
                    return {"email": user["email"], "password": user["password"]}
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            pass

        # Fallback to environment or defaults
        return {
            "email": os.getenv("TEST_USER_EMAIL", "test@example.com"),
            "password": os.getenv("TEST_USER_PASSWORD", "TestPassword123!")
        }