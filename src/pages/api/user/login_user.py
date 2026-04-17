"""
User API - Verify Login

API endpoint for user login verification.
Endpoint: POST /api/verifyLogin (API 7, 8, 9, 10 from documentation)
"""
import os

from playwright.sync_api import APIRequestContext, APIResponse


class LoginUser:
    """Page object for user login verification API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def post(self, email: str, password: str) -> APIResponse:
        """
        Verify login user with email and password.
        API 7: Returns 200 "User exists!"
        API 8: Returns 400 if missing email parameter
        API 10: Returns 404 "User not found!" for invalid credentials

        Args:
            email: User's email address
            password: User's password

        Returns:
            APIResponse object
        """
        return self.request.post(
            f"{self.BASE_URL}/api/verifyLogin",
            form={
                "email": email,
                "password": password
            }
        )