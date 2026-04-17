"""
User API - Delete Account

API endpoint for deleting user account.
Endpoint: DELETE /api/deleteAccount (API 12 from documentation)
"""
import os

from playwright.sync_api import APIRequestContext, APIResponse


class DeleteAccount:
    """Page object for deleting user account API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def delete(self, email: str, password: str) -> APIResponse:
        """
        Delete user account using DELETE method.
        API 12: Returns 200 "Account deleted!"

        Args:
            email: User's email address
            password: User's password

        Returns:
            APIResponse object
        """
        # API 12 requires DELETE method, not POST
        return self.request.delete(
            f"{self.BASE_URL}/api/deleteAccount",
            form={
                "email": email,
                "password": password
            }
        )