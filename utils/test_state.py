# tests/utils/context.py
import json
import logging
import os
from typing import Any, Optional


class TestContext:
    """
    Unified test state management for storing request/response data 
    and test data across test steps.
    
    This class provides both file-based persistence (for E2E tests)
    and in-memory storage (for API tests).
    """
    
    # In-memory storage for API tests
    _memory_data: dict = {}
    
    def __init__(self):
        self.directory = os.path.join("test-results", "test_state")
        self.logger = logging.getLogger(self.__class__.__name__)
        try:
            os.makedirs(self.directory, exist_ok=True)
        except (PermissionError, FileExistsError):
            pass

        self.pid = os.getpid()
        self.filepath = os.path.join(self.directory, f"e2e_data_worker_{self.pid}.json")
        self.data = {}

    def set(self, key: str, value: Any) -> None:
        """Store value in both file and memory"""
        # Check for APIResponse objects and extract serializable data
        if hasattr(value, '__class__') and value.__class__.__name__ == 'APIResponse':
            # This is an APIResponse object - extract all serializable parts
            try:
                value = {
                    "status": value.status,
                    "status_text": value.status_text,
                    "url": str(value.url) if value.url else None,
                    "json": value.json() if hasattr(value, 'json') and callable(value.json) else {}
                }
            except Exception:
                # If extraction fails, store minimal data
                value = {"status": getattr(value, 'status', None), "status_text": getattr(value, 'status_text', None)}
        
        self.data[key] = value
        TestContext._memory_data[key] = value
        self._write_file()

    def get_strict(self, key: str) -> Any:
        """Get value from memory, fall back to file if needed"""
        if key in TestContext._memory_data:
            return TestContext._memory_data[key]
        
        self._read_file()
        if key in self.data:
            TestContext._memory_data[key] = self.data[key]
            return self.data[key]
            
        raise KeyError(
            f"Key '{key}' not found for Worker {self.pid} in {self.filepath}. "
            "Check if the previous sequence step failed."
        )

    def get(self, key: str, default: Any = None) -> Any:
        """Get value with default fallback"""
        try:
            return self.get_strict(key)
        except KeyError:
            return default

    # === API Response Storage ===
    
    @property
    def last_response(self) -> dict:
        """Get last API response data"""
        return self.get("last_response", {})
    
    @last_response.setter
    def last_response(self, value: dict) -> None:
        """Set last API response data"""
        self.set("last_response", value)
        TestContext._memory_data["last_response"] = value

    def store_response(self, endpoint: str, response_data: dict) -> None:
        """Store response data by endpoint"""
        responses = self.get("responses", {})
        responses[endpoint] = response_data
        self.set("responses", responses)
        self.last_response = response_data

    def get_response(self, endpoint: str) -> Optional[dict]:
        """Retrieve response data for a specific endpoint"""
        responses = self.get("responses", {})
        return responses.get(endpoint)

    # === Test Data Storage (for user data from JSON) ===
    
    def set_data(self, key: str, value: Any) -> None:
        """Store arbitrary test data"""
        self.set(key, value)
        TestContext._memory_data[key] = value

    def get_data(self, key: str, default: Any = None) -> Any:
        """Retrieve stored test data"""
        return self.get(key, default)

    # === User Data Storage ===
    
    @property
    def last_created_user(self) -> Optional[dict]:
        """Get last created user data"""
        return self.get("last_created_user")
    
    @last_created_user.setter
    def last_created_user(self, value: dict) -> None:
        """Set last created user data"""
        self.set("last_created_user", value)
        TestContext._memory_data["last_created_user"] = value

    @property
    def last_created_order(self) -> Optional[dict]:
        """Get last created order data"""
        return self.get("last_created_order")
    
    @last_created_order.setter
    def last_created_order(self, value: dict) -> None:
        """Set last created order data"""
        self.set("last_created_order", value)
        TestContext._memory_data["last_created_order"] = value

    # === Cleanup ===
    
    def clear(self) -> None:
        """Clear all stored data"""
        self.last_response = {}
        self.set("responses", {})
        self.set("data", {})
        TestContext._memory_data.clear()

    def _write_file(self):
        try:
            # Filter out non-serializable objects
            serializable_data = {}
            for key, value in self.data.items():
                # Skip APIResponse objects (already handled in set())
                if hasattr(value, '__class__') and value.__class__.__name__ == 'APIResponse':
                    continue
                # Skip requests.Response objects by checking class name
                if hasattr(value, '__class__') and value.__class__.__name__ == 'Response':
                    continue
                # Skip any object with 'json' method that might be non-serializable
                if hasattr(value, '__dict__') and 'json' in value.__class__.__name__.lower():
                    continue
                serializable_data[key] = value
            
            with open(self.filepath, 'w') as f:
                json.dump(serializable_data, f, indent=4)
        except PermissionError:
            self.logger.warning("Unable to write test state file: %s", self.filepath)
        except (TypeError, ValueError) as e:
            self.logger.warning("Unable to serialize test state data: %s", e)

    def _read_file(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    self.data = json.load(f)
            except PermissionError:
                self.logger.warning("Unable to read test state file: %s", self.filepath)

    def cleanup(self):
        """Clean up test state files"""
        if os.path.exists(self.filepath):
            try:
                os.remove(self.filepath)
            except PermissionError:
                self.logger.warning("Unable to delete test state file: %s", self.filepath)


# Global instance for use across all test steps
context = TestContext()

# Alias for backward compatibility
test_context = context
