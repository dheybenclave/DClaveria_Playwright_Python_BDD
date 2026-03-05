import logging
import re
from pathlib import Path
from time import sleep

from playwright.sync_api import Page, expect, Locator

from src.pages.base_page import BasePage
from utils.config import Config


class CommonPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.logger = logging.getLogger("Framework")

    # Locators
    def lbl_text(self, text, is_exact_value: bool = None) -> Locator:
        return self.page.get_by_text(text, exact=is_exact_value)

    def nav_menu_items(self) -> Locator:
        return self.page.locator(f'//nav[@class="navbar"]/a[@href]')

    def get_locator_by(self, locator_type: str, locator_value: str, parent_selector: str = None) -> Locator:
        scope = self.page.locator(parent_selector) if parent_selector else self.page

        locators = {
            "alt_text": scope.get_by_alt_text,
            "label": scope.get_by_label,
            "placeholder": scope.get_by_placeholder,
            "role": scope.get_by_role,
            "test_id": scope.get_by_test_id,
            "text": scope.get_by_text,
            "title": scope.get_by_title,
            "xpath": scope.locator,
            "css": scope.locator,
        }

        locator_func = locators.get(locator_type, scope.locator)
        return locator_func(locator_value)

        # Commands

    def open_browser(self, target: str):
        self.logger.debug(f"Opening Browser {target}")
        url = f"{Config.BASE_URL}{target}" if target else Config.BASE_URL
        self.page.goto(url, wait_until="domcontentloaded", timeout=15000)
        self.page.wait_for_load_state()
        return self.page

    def navigate_to_by_text(self, target: str):
        self.logger.debug(f"Navigating using text {target}")
        self.nav_menu_items().filter(has_text=target).click()

    def focus_element(self, locator: Locator):
        self.logger.debug(f"Focus Element {locator}")

        self.verify_element_visible(locator)
        locator.focus()
        expect(locator).to_be_focused()
        return locator

    def click_element(self, locator: Locator):
        self.logger.debug(f"Click Element {locator}")

        self.verify_element_visible(locator)
        locator.scroll_into_view_if_needed()
        locator.click()
        return locator

    def click_element_by_text(self, text_to_click: str, parent_selector: str = None):
        self.logger.debug(f"Click Element {text_to_click} with selector '{parent_selector}'")

        locator = self.get_locator_by("text", text_to_click, parent_selector)
        self.verify_element_visible(locator)
        locator.click()

    def enter_text(self, locator: Locator, value: str):
        self.logger.debug(f"Enter Text {locator}")

        self.focus_element(locator)
        locator.fill("")
        locator.fill(value)
        self.verify_element_value(locator, value)
        return locator

    def press_key_element(self, locator: Locator, key_press: str):
        self.logger.debug(f"Press Key {key_press} in {locator} ")

        self.focus_element(locator)
        locator.press(key_press, delay=1500)
        return locator

    # Assertions

    def verify_text_visible(self, text, is_exact_text: bool = None):
        self.logger.debug(f"Verifying text visible: '{text}'")

        locator = self.lbl_text(text, is_exact_text)
        locator.scroll_into_view_if_needed()
        expect(locator).to_be_visible()
        assert locator.is_visible()

    def verify_element_visible(self, locator: Locator):
        self.logger.debug(f"Verifying element visible: '{locator}'")

        locator.scroll_into_view_if_needed()
        expect(locator).to_be_visible()
        assert locator.is_visible()

    def verify_element_not_visible(self, locator: Locator):
        self.logger.debug(f"Verifying element not visible: '{locator}'")

        expect(locator).not_to_be_visible()
        assert locator.is_hidden()

    def verify_element_attribute(self, locator: Locator, attr_name: str, expected_attr_value: str):
        self.logger.debug(f"Verifying element attribute: '{attr_name}' ({expected_attr_value})")

        get_value = locator.get_attribute(attr_name)
        self.logger.debug(
            f"Getting attribute: Attribute Name :'{attr_name}' | Attribute Value :' {expected_attr_value}'")
        assert expected_attr_value in get_value

    def verify_element_value(self, locator: Locator, expected_value: str):
        ex_value = re.compile(rf".*{re.escape(expected_value)}.*", re.IGNORECASE)
        el_value = locator.input_value()

        self.logger.debug(f"Verifying element : Expected Value: '{ex_value}' | Actual Value : '{el_value}'")

        expect(locator).to_have_value(ex_value)

    def upload_file(self, locator: Locator, file_name: str, file_type: str):
        self.logger.debug(f"Uploading file '{locator}' to file '{file_name}'")

        current_dir = Path(__file__).parent

        file_path = current_dir.parent.parent / "test_data" / f"{file_name}.{file_type}"

        locator.set_input_files(file_path)
        self.verify_element_value(locator, file_name)
        sleep(1.5)

    # Universal api_suites Method

    def api_call(self, request_context, method, endpoint, **kwargs):
        self.logger.debug(f"API {method} request to {endpoint}")
        return request_context.fetch(endpoint, method=method, **kwargs)
