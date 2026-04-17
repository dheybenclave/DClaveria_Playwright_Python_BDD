"""
Order API - Create Order

API endpoint for creating an order.
Endpoint: POST /api/createOrder
"""
import os

from playwright.sync_api import APIRequestContext, APIResponse


class CreateOrder:
    """Page object for creating order API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def post(
        self,
        name: str,
        email: str,
        phone: str,
        address: str,
        city: str,
        state: str,
        country: str,
        zipcode: str,
        payment_method: str = "COD",
        credit_card_number: str = "",
        card_number: str = "",
        card_exp_month: str = "",
        card_exp_year: str = "",
        card_cvv: str = ""
    ) -> APIResponse:
        """
        Create a new order.

        Args:
            name: Customer name
            email: Customer email
            phone: Phone number
            address: Address
            city: City
            state: State
            country: Country
            zipcode: Zipcode
            payment_method: Payment method (COD, Credit Card)
            credit_card_number: Credit card number (legacy)
            card_number: Card number
            card_exp_month: Card expiry month
            card_exp_year: Card expiry year
            card_cvv: Card CVV

        Returns:
            APIResponse object
        """
        data = {
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "city": city,
            "state": state,
            "country": country,
            "zipcode": zipcode,
            "payment_method": payment_method,
        }

        # Add credit card details if provided
        if credit_card_number:
            data["credit_card_number"] = credit_card_number
        if card_number:
            data["card_number"] = card_number
        if card_exp_month:
            data["card_exp_month"] = card_exp_month
        if card_exp_year:
            data["card_exp_year"] = card_exp_year
        if card_cvv:
            data["card_cvv"] = card_cvv

        return self.request.post(
            f"{self.BASE_URL}/api/createOrder",
            form=data
        )

    def post_cod(self, name: str, email: str, phone: str, address: str, city: str, state: str, country: str, zipcode: str) -> APIResponse:
        """Create order with Cash on Delivery"""
        return self.post(
            name=name, email=email, phone=phone,
            address=address, city=city, state=state,
            country=country, zipcode=zipcode,
            payment_method="COD"
        )