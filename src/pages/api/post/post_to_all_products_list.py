import logging

from playwright.sync_api import APIRequestContext

from utils.config import Config


class PostToAllProductsList:
    def __init__(self, request: APIRequestContext):
        self.request = request
        self.logger = logging.getLogger("Framework")

    def post_to_products_list(self):
        self.logger.debug("Sending POST request to products list")
        return self.request.post(f"{Config.BASE_URL}/api/productsList")

    def verify_response_status_code(self, response_data, status_code):
        self.logger.debug(f"Verifying response status code: {status_code}")
        response_json = response_data.json()
        get_status = response_json.get("responseCode")
        assert get_status == status_code, f"Expected {status_code}, but got {get_status}"

    def verify_message(self, response_data, expected_message):
        self.logger.debug(f"Verifying response message: {expected_message}")
        response_json = response_data.json()
        message = response_json.get("message", "")
        assert expected_message in message, f"Expected message '{expected_message}', got: {message}"