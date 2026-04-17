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

    # User API endpoints
    @property
    def create_account(self):
        from src.pages.api.user.create_account import CreateAccount
        return CreateAccount(self.request)

    @property
    def login_user(self):
        from src.pages.api.user.login_user import LoginUser
        return LoginUser(self.request)

    @property
    def get_user_detail_by_email(self):
        from src.pages.api.user.get_user_detail_by_email import GetUserDetailByEmail
        return GetUserDetailByEmail(self.request)

    @property
    def update_account(self):
        from src.pages.api.user.update_account import UpdateAccount
        return UpdateAccount(self.request)

    @property
    def delete_account(self):
        from src.pages.api.user.delete_account import DeleteAccount
        return DeleteAccount(self.request)

    # Order API endpoints
    @property
    def create_order(self):
        from src.pages.api.order.create_order import CreateOrder
        return CreateOrder(self.request)

    @property
    def get_order_by_order_id(self):
        from src.pages.api.order.get_order_by_order_id import GetOrderByOrderId
        return GetOrderByOrderId(self.request)

    @property
    def get_orders(self):
        from src.pages.api.order.get_orders import GetOrders
        return GetOrders(self.request)

    # Search API endpoints
    @property
    def search_product(self):
        from src.pages.api.search.search_product import SearchProduct
        return SearchProduct(self.request)
