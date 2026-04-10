import logging

from playwright.sync_api import APIRequestContext


class ApiBasePage:
    def __init__(self, request: APIRequestContext):
        self.request = request
        self.logger = logging.getLogger(self.__class__.__name__)

    # @property
    # def base_api(self):
    #     return BaseApi(self.page)

    @property
    def all_products(self):
        # Local import avoids circular import with LoginPage(BasePage).
        from src.pages.api.get.get_all_product_list import GetAllProductList
        return GetAllProductList(self.request)

    @property
    def get_all_brands_list(self):
        from src.pages.api.get.get_all_brands_list import GetAllBrandsList
        return GetAllBrandsList(self.request)

    @property
    def post_to_all_products_list(self):
        from src.pages.api.post.post_to_all_products_list import PostToAllProductsList
        return PostToAllProductsList(self.request)
