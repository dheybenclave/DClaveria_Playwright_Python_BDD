import csv
import logging

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import UIBasePage
from utils.config import Config
from utils.test_state import context


class LoginPage(UIBasePage):
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

    @property
    def btn_logout(self) -> Locator:
        return self.page.locator("a[href='/logout']")

    @property
    def btn_continue(self) -> Locator:
        return self.page.locator("a[data-qa='continue-button']")

    def navigate_to_login_page(self) -> "LoginPage":
        """Navigate to the login page"""
        self.logger.info("Navigating to login page")
        self.page.goto(f"{Config.BASE_URL}/login", wait_until="domcontentloaded")
        return self

    def get_credentials_by_role(self, role: str):
        file_path = "tests/test_datas/excel_file/user_credentials.csv"

        with open(file_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row.get('role') == role:
                    return row['username'], row['password']

        raise ValueError(f"Role '{role}' not found in CSV file.")

    def login_credentials_by_role(self, role: str = None) -> None:
        """
        Authenticates a user based on their role, searching through:
        1. GitHub JSON Secret (CI/CD)
        2. Local .env variables (Dev)
        3. Excel Database (Legacy/Fallback)
        """
        self.logger.info(f"Initiating login sequence for role: '{role}'")

        try:
            # 1. Attempt to fetch from Config (covers JSON Secret and .env Fallback)
            creds = Config.get_credentials(role)
            username = creds["email"]
            password = creds["password"]  # Map the 'password' from JSON or 'PASSWORD' from .env
            found_by = "Cloud/Env Config"

        except (EnvironmentError, ValueError, KeyError) as e:
            self.logger.warning(f"Config lookup failed for '{role}': {e}. Trying Excel...")

            # 2. Fallback to local Excel logic
            try:
                username, password = self.get_credentials_by_role(role)
                found_by = "Excel File"
            except Exception as excel_err:
                self.logger.error(f"Final fallback failed. No credentials found for '{role}'")
                raise excel_err

        # Masking the username for secure logging (e.g., adm***@test.com)
        masked_user = f"{username[:3]}***{username[username.find('@'):]}" if "@" in username else "***"
        self.logger.info(f"Successfully retrieved credentials via {found_by} for {role} ({masked_user})")

        # UI Interaction
        self.common_page.enter_text(self.txt_username, username)
        self.common_page.enter_text(self.txt_password, password)
        self.btn_login.click(timeout=15000)

    def login_credentials(self, username: str, password: str) -> None:
        self.logger.info(f"Credentials found using username and password")
        self.common_page.enter_text(self.txt_username, username)
        self.common_page.enter_text(self.txt_password, password)
        self.btn_login.click()

    def login_credential_with_created_user(self) -> None:
        self.logger.info(f"Credentials found using username and password to create user")

        self.common_page.click_element(self.btn_continue)
        self.page.wait_for_load_state()

        self.common_page.click_element(self.btn_logout)
        self.page.wait_for_load_state()

        expect(self.txt_username).to_be_visible(timeout=10000)

        self.common_page.enter_text(self.txt_username, context.get_strict("email"))
        self.common_page.enter_text(self.txt_password, context.get_strict("password"))
        self.btn_login.click()

    def enter_login_username(self, username: str) -> None:
        """Enter username in login form"""
        self.common_page.enter_text(self.txt_username, username)

    def enter_login_password(self, password: str) -> None:
        """Enter password in login form"""
        self.common_page.enter_text(self.txt_password, password)

    def click_login_button(self) -> None:
        """Click login button"""
        self.btn_login.click()
