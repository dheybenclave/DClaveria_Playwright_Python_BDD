import logging

from playwright.sync_api import APIRequestContext

from utils.config import Config


class GetAllBrandsList:
    def __init__(self, request: APIRequestContext):
        self.request = request
        self.logger = logging.getLogger("Framework")

    def get_all_brands(self):
        self.logger.debug("Getting all brands")
        return self.request.get(f"{Config.BASE_URL}/api/brandsList")

    def verify_response_status_code(self, response_data, status_code):
        self.logger.debug(f"Verifying response status code: {status_code}")
        response_json = response_data.json()
        get_status = response_json.get("responseCode")
        assert get_status == status_code, f"Expected {status_code}, but got {get_status}"

    def verify_performance_of_response(self, duration_ms, limit):
        self.logger.debug(f"Verifying response performance: {duration_ms} | Limit: {limit}")
        assert duration_ms is not None
        assert duration_ms < limit, f"Performance Failure: {duration_ms}ms exceeded limit of {limit}ms"
