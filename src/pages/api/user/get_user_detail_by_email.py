"""
User API - Get User Detail By Email

API endpoint for getting user details by email.
Endpoint: GET /api/getUserDetailByEmail
"""
import os

from playwright.sync_api import APIRequestContext, APIResponse


class GetUserDetailByEmail:
    """Page object for getting user details by email API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def get(self, email: str) -> APIResponse:
        """
        Get user details by email.

        Args:
            email: User's email address

        Returns:
            APIResponse object
        """
        return self.request.get(
            f"{self.BASE_URL}/api/getUserDetailByEmail",
            params={"email": email}
        )