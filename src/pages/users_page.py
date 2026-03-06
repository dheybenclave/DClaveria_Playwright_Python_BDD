from playwright.sync_api import Page, expect
from src.pages.base_page import BasePage
from src.pages.common_page import CommonPage


class UserPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Selectors for the specific website
        self.search_bar = page.get_by_placeholder("Search users...")
        self.user_rows = page.locator("table tbody tr")

    def search_and_verify_user(self, name: str, email: str, role: str):
        # 1. Search for the user
        self.search_bar.fill(name)
        self.page.keyboard.press("Enter")

        # 2. Locate the specific row containing the email
        # We use the email as a unique anchor for the row
        target_row = self.user_rows.filter(has_text=email)

        # 3. Assertions (Auto-waiting included)
        expect(target_row).to_be_visible()
        expect(target_row).to_contain_text(name)
        expect(target_row).to_contain_text(role)



