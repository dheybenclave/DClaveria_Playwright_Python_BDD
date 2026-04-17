"""
User API - Create Account

API endpoint for creating a new user account.
Endpoint: POST /api/createAccount
"""
import os
from typing import Dict, Optional

from playwright.sync_api import APIRequestContext, APIResponse


class CreateAccount:
    """Page object for user account creation API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def post(
        self,
        name: str,
        email: str,
        password: str,
        title: str = "Mr",
        birth_day: str = "1",
        birth_month: str = "January",
        birth_year: str = "1990",
        firstname: str = "",
        lastname: str = "",
        company: str = "",
        address1: str = "",
        address2: str = "",
        country: str = "United States",
        city: str = "",
        state: str = "",
        zipcode: str = "",
        mobile_number: str = ""
    ) -> APIResponse:
        """
        Create a new user account.

        Args:
            name: User's name
            email: User's email address
            password: User's password
            title: Title (Mr, Mrs, Miss, Ms)
            birth_day: Birth day
            birth_month: Birth month
            birth_year: Birth year
            firstname: First name
            lastname: Last name
            company: Company name
            address1: Address line 1
            address2: Address line 2
            country: Country
            city: City
            state: State
            zipcode: Zipcode
            mobile_number: Mobile phone number

        Returns:
            APIResponse object
        """
        data = {
            "name": name,
            "email": email,
            "password": password,
            "title": title,
            "birth_day": birth_day,
            "birth_month": birth_month,
            "birth_year": birth_year,
            "firstname": firstname,
            "lastname": lastname,
            "company": company,
            "address1": address1,
            "address2": address2,
            "country": country,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "mobile_number": mobile_number
        }

        return self.request.post(
            f"{self.BASE_URL}/api/createAccount",
            form=data
        )

    def post_required_only(self, name: str, email: str, password: str) -> APIResponse:
        """Create account with only required fields"""
        return self.request.post(
            f"{self.BASE_URL}/api/createAccount",
            data={"name": name, "email": email, "password": password}
        )