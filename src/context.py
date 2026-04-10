"""
Global test context for storing request/response data across test steps.

This module provides a global object that can be used to share data between
different step definitions, making it easy to access response data for
regression testing and debugging.

Usage:
    from src.context import test_context
    
    # After making an API request
    test_context.last_response = {"json": {...}, "status": 200}
    
    # Access in another step
    data = test_context.last_response
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class TestContext:
    """Global test context for storing request/response data."""
    
    # Last API response data
    last_response: Optional[dict[str, Any]] = field(default_factory=dict)
    
    # Store multiple responses by endpoint
    responses: dict[str, dict[str, Any]] = field(default_factory=dict)
    
    # Test data storage
    data: dict[str, Any] = field(default_factory=dict)
    
    def store_response(self, endpoint: str, response_data: dict[str, Any]) -> None:
        """Store response data by endpoint for later retrieval."""
        self.responses[endpoint] = response_data
        self.last_response = response_data
    
    def get_response(self, endpoint: str) -> Optional[dict[str, Any]]:
        """Retrieve response data for a specific endpoint."""
        return self.responses.get(endpoint)
    
    def set_data(self, key: str, value: Any) -> None:
        """Store arbitrary test data."""
        self.data[key] = value
    
    def get_data(self, key: str, default: Any = None) -> Any:
        """Retrieve stored test data."""
        return self.data.get(key, default)
    
    def clear(self) -> None:
        """Clear all stored data."""
        self.last_response = {}
        self.responses.clear()
        self.data.clear()


# Global instance for use across all test steps
test_context = TestContext()
