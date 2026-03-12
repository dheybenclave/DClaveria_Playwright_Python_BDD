from __future__ import annotations

import logging
from functools import cached_property
from typing import TYPE_CHECKING

from playwright.sync_api import Page

from utils.utils import Utility

if TYPE_CHECKING:
    from src.pages.common_page import CommonPage
    from src.pages.login_page import LoginPage
    from src.pages.sign_up_page import SignUpPage


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logging.getLogger(self.__class__.__name__)

    @cached_property
    def utils(self) -> Utility:
        return Utility()

    @cached_property
    def common_page(self) -> "CommonPage":
        from src.pages.common_page import CommonPage
        return CommonPage(self.page)

    @cached_property
    def login_page(self) -> "LoginPage":
        from src.pages.login_page import LoginPage
        return LoginPage(self.page)

    @cached_property
    def sign_up_page(self) -> "SignUpPage":
        from src.pages.sign_up_page import SignUpPage
        return SignUpPage(self.page)


