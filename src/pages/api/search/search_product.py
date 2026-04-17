"""
Search API - Search Product

API endpoint for searching products.
Endpoint: POST /api/searchProduct (API 5 from documentation)
"""
import os
from typing import Optional

from playwright.sync_api import APIRequestContext, APIResponse


class SearchProduct:
    """Page object for searching products API"""

    BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com")

    def __init__(self, request: APIRequestContext):
        self.request = request

    def get(self, search_query: str) -> APIResponse:
        """
        Search for products using POST method.

        Args:
            search_query: Search query string

        Returns:
            APIResponse object
        """
        # API 5 uses POST method with search_product as form field
        return self.request.post(
            f"{self.BASE_URL}/api/searchProduct",
            form={"search_product": search_query}
        )

    def post(self, search_query: str) -> APIResponse:
        """Search products using POST method (explicit)"""
        return self.request.post(
            f"{self.BASE_URL}/api/searchProduct",
            form={"search_product": search_query}
        )

    def get_by_category(self, category: str) -> APIResponse:
        """Search products by category"""
        return self.get(f"category:{category}")

    def get_by_brand(self, brand: str) -> APIResponse:
        """Search products by brand"""
        return self.get(f"brand:{brand}")