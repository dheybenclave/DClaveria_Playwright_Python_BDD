import logging

from playwright.sync_api import APIRequestContext

from utils.config import Config


class GetAllProductList:  # Must match the loader's "class_name"
    def __init__(self, request: APIRequestContext):
        self.request = request
        self.logger = logging.getLogger("Framework")

    def get_all_products(self):
        self.logger.debug("Getting all products")
        return self.request.get(f"{Config.BASE_URL}/api/productsList")

    def get_response_json(self, response):
        self.logger.debug(f"Response JSON: {response}")
        # Playwright APIResponse exposes json() for body parsing.
        if hasattr(response, "json"):
            return response.json()
        if isinstance(response, dict) and "json" in response:
            return response["json"]
        raise TypeError(f"Unsupported response type for JSON parsing: {type(response)}")

    def validate_product_structure(self, response_json, required_keys):
        self.logger.debug("Validating product structure")
        products = response_json.get("products", [])

        for product in products:
            for key in required_keys:
                self.logger.debug(f"Product {key} found in {product}")
                assert key in product, f'Missing key "{key}" in product: {product}'

    def verify_performance_of_response(self, duration_ms, limit):
        self.logger.debug(f"Verifying performance of the Response Data : {duration_ms} | Limit : {limit}")
        assert duration_ms is not None
        assert duration_ms < limit, f"Performance Failure: {duration_ms}ms exceeded limit of {limit}ms"

    def verify_response_status_code(self, response_data, status_code):
        self.logger.debug(f"Verifying response status code: {status_code}")

        response_json = response_data.json()

        get_status = response_json.get("responseCode")  # Ensure this matches the API's actual key name

        assert get_status == status_code, f"Expected {status_code}, but got {get_status}"
