import csv
import logging

from playwright.sync_api import Locator, Page

from src.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    # ===============================================================================================
    # Locators
    # ===============================================================================================

    @property
    def txt_username(self) -> Locator:
        return self.page.locator("[data-qa='login-email']")

    @property
    def txt_password(self) -> Locator:
        return self.page.locator("[data-qa='login-password']")

    @property
    def btn_login(self) -> Locator:
        return self.page.locator("button[data-qa='login-button']")

    # ===============================================================================================
    # Commands
    # ===============================================================================================

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

    def login_credentials(self, role: str = None, username: str = None, password: str = None) -> None:

        self.logger.debug(f"Attempting login with role='{role}', username='{username}'")

        if role:
            username, password = self.get_credentials_by_role(role)
        elif not (username and password):
            raise ValueError("You must provide either a 'role' or both 'username' and 'password'.")

        self.common_page.verify_element_visible(self.txt_username)
        self.txt_username.fill(username)

        self.common_page.verify_element_visible(self.txt_password)
        self.txt_password.fill(password)

        self.common_page.verify_element_visible(self.btn_login)
        self.btn_login.click()
