"""
User API - Update Account

API endpoint for updating user account.
Endpoint: PUT /api/updateAccount
"""
import os
from typing import Dict

from playwright.sync_api import APIRequestContext, APIResponse


class UpdateAccount:
    """Page object for updating user account API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def put(
        self,
        email: str,
        password: str,
        new_password: str = None,
        name: str = None,
        title: str = None,
        birth_day: str = None,
        birth_month: str = None,
        birth_year: str = None,
        firstname: str = None,
        lastname: str = None,
        company: str = None,
        address1: str = None,
        address2: str = None,
        country: str = None,
        city: str = None,
        state: str = None,
        zipcode: str = None,
        mobile_number: str = None
    ) -> APIResponse:
        """
        Update user account.

        Args:
            email: Current user's email (required)
            password: Current password (required)
            new_password: New password (optional)
            name: User's name (optional)
            title: Title (optional)
            birth_day: Birth day (optional)
            birth_month: Birth month (optional)
            birth_year: Birth year (optional)
            firstname: First name (optional)
            lastname: Last name (optional)
            company: Company name (optional)
            address1: Address line 1 (optional)
            address2: Address line 2 (optional)
            country: Country (optional)
            city: City (optional)
            state: State (optional)
            zipcode: Zipcode (optional)
            mobile_number: Mobile phone number (optional)

        Returns:
            APIResponse object
        """
        data = {
            "email": email,
            "password": password
        }

        # Add optional fields if provided
        if new_password:
            data["new_password"] = new_password
        if name:
            data["name"] = name
        if title:
            data["title"] = title
        if birth_day:
            data["birth_day"] = birth_day
        if birth_month:
            data["birth_month"] = birth_month
        if birth_year:
            data["birth_year"] = birth_year
        if firstname:
            data["firstname"] = firstname
        if lastname:
            data["lastname"] = lastname
        if company:
            data["company"] = company
        if address1:
            data["address1"] = address1
        if address2:
            data["address2"] = address2
        if country:
            data["country"] = country
        if city:
            data["city"] = city
        if state:
            data["state"] = state
        if zipcode:
            data["zipcode"] = zipcode
        if mobile_number:
            data["mobile_number"] = mobile_number

        return self.request.put(
            f"{self.BASE_URL}/api/updateAccount",
            form=data
        )