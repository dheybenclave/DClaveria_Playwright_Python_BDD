import csv
import logging

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage
from utils.config import Config
from utils.test_state import context


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def txt_username(self) -> Locator:
        return self.page.locator("[data-qa='login-email']")

    @property
    def txt_password(self) -> Locator:
        return self.page.locator("[data-qa='login-password']")

    @property
    def btn_login(self) -> Locator:
        return self.page.locator("button[data-qa='login-button']")

    def get_credentials_by_role(self, role: str):
        file_path = "tests/test_datas/excel_file/user_credentials.csv"

        with open(file_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row.get('role') == role:
                    return row['username'], row['password']

        raise ValueError(f"Role '{role}' not found in CSV file.")

    def login_credentials_by_role(self, role: str = None) -> None:
        self.logger.debug(f"Credentials found using {role}")
        try:
            # 1. Try JSON credentials from GitHub Secret
            creds = Config.get_credentials(role)
            username, password = creds["email"], creds["password"]
            found_by = "GitHub JSON > .env Secret"
        except (EnvironmentError, ValueError):
            # 2. Fallback to your Excel/local logic
            username, password = self.get_credentials_by_role(role)
            found_by = "Excel File"

        self.logger.debug(f"Credentials found using {found_by}")
        self.common_page.enter_text(self.txt_username, username)
        self.common_page.enter_text(self.txt_password, password)
        self.btn_login.click()

    def login_credentials(self, username: str, password: str) -> None:
        self.logger.debug(f"Credentials found using username and passowerd")
        self.common_page.enter_text(self.txt_username, username)
        self.common_page.enter_text(self.txt_password, password)
        self.btn_login.click()

    def login_credential_with_created_user(self) -> None:
        self.logger.debug(f"Credentials found using username and password to create user")
        try:
            visible = self.txt_username.is_visible(timeout=3000)
        except Exception:
            visible = False

        if not visible:
            self.common_page.open_browser("/login")
            login_link = self.page.get_by_role("link", name="Signup / Login")
            logout_link = self.page.get_by_role("link", name="Logout")

            if logout_link.count() > 0:
                logout_link.first.click()
                login_link = self.page.get_by_role("link", name="Signup / Login")

            if login_link.count() > 0:
                login_link.first.click()
            else:
                self.common_page.open_browser("/login")

            expect(self.txt_username).to_be_visible(timeout=10000)

        self.common_page.enter_text(self.txt_username, context.get_strict("email"))
        self.common_page.enter_text(self.txt_password, context.get_strict("password"))
        self.btn_login.click()
