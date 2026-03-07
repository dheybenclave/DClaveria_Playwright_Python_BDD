import csv
import logging

from playwright.sync_api import Locator, Page

from src.pages.base_page import BasePage
from utils.config import Config


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
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
        self.logger.debug(f"Getting credentials by role '{role}'")
        file_path = "tests/test_datas/user_credentials.csv"
        with open(file_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row.get('role') == role:
                    self.logger.debug(f"Found credentials for role '{role}': username='{row['username']}'")
                    return row['username'], row['password']

        raise ValueError(f"Role '{role}' not found in CSV file.")

    def login_credentials_by_role(self, role: str = None) -> None:

        self.logger.debug(f"Attempting login with role='{role}''")

        try:
            creds = Config.get_credentials_env(role)
            resolved_username = creds["email"]
            resolved_password = creds["password"]
            self.logger.debug(f"Found credentials via .env for role '{role}''")
        except EnvironmentError:
            resolved_username, resolved_password = self.get_credentials_by_role(role)
            self.logger.debug(f"Found credentials for csv file for role '{role}''")

        self.common_page.enter_text(self.txt_username, resolved_username)
        self.common_page.enter_text(self.txt_password, resolved_password)
        self.btn_login.click(timeout=15000)
