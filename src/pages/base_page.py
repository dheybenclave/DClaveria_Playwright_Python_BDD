import logging

from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    # @property
    # def base_page(self):
    #     return BasePage(self.page)

    @property
    def common_page(self):
        # Local import avoids circular import with CommonPage(BasePage).
        from src.pages.common_page import CommonPage
        return CommonPage(self.page)

    @property
    def login_page(self):
        # Local import avoids circular import with LoginPage(BasePage).
        from src.pages.login_page import LoginPage
        return LoginPage(self.page)


