import logging

from playwright.sync_api import Locator, Page, expect

from src.pages.base_page import BasePage
from utils.test_state import context


class SignUpPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def txt_sign_up_name(self) -> Locator:
        return self.page.locator("[data-qa='signup-name']")

    @property
    def txt_sign_up_email(self) -> Locator:
        return self.page.locator("[data-qa='signup-email']")

    @property
    def txt_password(self) -> Locator:
        return self.page.locator("[data-qa='password']")

    @property
    def btn_sign_up(self) -> Locator:
        return self.page.locator("[data-qa='signup-button']")

    @property
    def opt_btn_title(self) -> Locator:
        return self.page.locator("//label[text()='Title']/parent::div")

    @property
    def btn_create_account(self) -> Locator:
        return self.page.locator("button[data-qa='create-account']")

    def create_new_user_by_sign_up(self, user_id: str):
        test_data = self.utils.get_json_data("register_user_data.json", user_id)
        gen_ran = self.utils.random_string(5)

        generated_email = f"dhytesting_{gen_ran}@test.com"
        context.set("email", generated_email)
        generated_password = f"pass_{gen_ran}_dhytesting"
        context.set("password", generated_password)
        generate_name = test_data["firstname"]
        context.set("firstname", generate_name)

        self.common_page.enter_text(self.txt_sign_up_name, generate_name)
        self.common_page.enter_text(self.txt_sign_up_email, generated_email)
        self.btn_sign_up.click()

        self.page.wait_for_load_state("domcontentloaded", timeout=10000)
        expect(self.common_page.lbl_text("Enter Account Information")).to_be_visible()
        self.page.check(f"[value='{test_data['title']}']")

        def _normalize(value, default):
            try:
                return str(int(str(value).lstrip("0") or default))
            except (TypeError, ValueError):
                return str(default)

        day_value = _normalize(test_data.get("birth_date"), 1)
        month_value = _normalize(test_data.get("birth_month"), 1)
        year_value = _normalize(test_data.get("birth_year"), 2000)

        expect(self.page.locator("#days")).to_be_enabled()
        expect(self.page.locator("#months")).to_be_enabled()
        expect(self.page.locator("#years")).to_be_enabled()

        self.page.select_option("#days", day_value)
        self.page.select_option("#months", month_value)
        self.page.select_option("#years", year_value)

        address_fields = {
            '#first_name': 'firstname',
            '#last_name': 'lastname',
            '#company': 'company',
            '#address1': 'address1',
            '#address2': 'address2',
            '#state': 'state',
            '#city': 'city',
            '#zipcode': 'zipcode',
            '#mobile_number': 'mobile_number'
        }

        for locator, json_key in address_fields.items():
            self.common_page.enter_text(locator, str(test_data[json_key]))

        self.common_page.enter_text(self.txt_password, generated_password)
        self.btn_create_account.click()
        self.page.wait_for_load_state()
