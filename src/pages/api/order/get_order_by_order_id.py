"""
Order API - Get Order By Order ID

API endpoint for getting order details by order ID.
Endpoint: GET /api/getOrderByOrderId
"""
import os

from playwright.sync_api import APIRequestContext, APIResponse


class GetOrderByOrderId:
    """Page object for getting order by order ID API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def get(self, order_id: str) -> APIResponse:
        """
        Get order details by order ID.

        Args:
            order_id: Order ID

        Returns:
            APIResponse object
        """
        return self.request.get(
            f"{self.BASE_URL}/api/getOrderByOrderId",
            params={"id": order_id}
        )