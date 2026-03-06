import logging

from playwright.sync_api import APIRequestContext


class BaseApi:
    def __init__(self, request: APIRequestContext):
        self.request = request
        self.logger = logging.getLogger(self.__class__.__name__)

    # @property
    # def base_api(self):
    #     return BaseApi(self.page)

    @property
    def get_all_product_list(self):
        # Local import avoids circular import with LoginPage(BasePage).
        from src.pages.api.get.get_all_product_list import GetAllProductList
        return GetAllProductList(self.request)
