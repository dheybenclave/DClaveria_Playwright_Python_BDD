"""
Order API - Get Orders

API endpoint for getting all orders.
Endpoint: GET /api/getOrders
"""
import os

from playwright.sync_api import APIRequestContext, APIResponse


class GetOrders:
    """Page object for getting all orders API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def get(self) -> APIResponse:
        """
        Get all orders.

        Returns:
            APIResponse object
        """
        return self.request.get(
            f"{self.BASE_URL}/api/getOrders"
        )