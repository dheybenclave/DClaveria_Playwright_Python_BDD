import logging
import re
from pathlib import Path

from playwright.sync_api import Page, expect, Locator

from src.pages.base_page import BasePage
from utils.config import Config


class CommonPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    def lbl_text(self, text, exact: bool = False) -> Locator:
        return self.page.get_by_text(text, exact=exact)

    def nav_menu_items(self) -> Locator:
        return self.page.locator('ul.navbar-nav li a[href]')

    def _get_locator(self, locator: str | Locator) -> Locator:
        return self.page.locator(locator) if isinstance(locator, str) else locator

    def open_browser(self, target: str = ""):
        self.logger.info(f"Opening Browser {target}")
        url = f"{Config.BASE_URL}{target}" if target else Config.BASE_URL
        self.page.goto(url, wait_until="domcontentloaded", timeout=15000)
        self.page.wait_for_load_state()
        return self.page

    def navigate_to_by_text(self, target: str):
        self.logger.info(f"Navigating using text {target}")
        self.nav_menu_items().filter(has_text=target).click()
        self.page.wait_for_load_state("domcontentloaded", timeout=15000)
        return self.page

    def focus_element(self, locator: str | Locator):
        self.logger.info(f"Focus Element {locator}")
        locator = self._get_locator(locator)
        self.verify_element_visible(locator)
        locator.focus()
        expect(locator).to_be_focused()
        return locator

    def click_element(self, locator: str | Locator):
        self.logger.info(f"Click Element {locator}")
        locator = self._get_locator(locator)
        self.verify_element_visible(locator)
        locator.scroll_into_view_if_needed()
        locator.click()
        return locator

    def click_element_by_text(self, text_to_click: str, parent_selector: str = None):
        self.logger.info(f"Click Element {text_to_click}")

        locator = self.page.locator(parent_selector).get_by_text(text_to_click) \
            if parent_selector else self.lbl_text(text_to_click, True)

        locator.wait_for(state="attached", timeout=5000)

        self.verify_element_visible(locator)

        try:
            locator.click(force=True, timeout=5000)
        except Exception:
            locator.evaluate("el => el.click()")

    def enter_text(self, locator: str | Locator, value: str):
        self.logger.info(f"Enter Text {locator}")
        locator = self._get_locator(locator)
        self.focus_element(locator)
        locator.fill(value)
        self.verify_element_value(locator, value)
        return locator

    def press_key_element(self, locator: str | Locator, key_press: str):
        self.logger.info(f"Press Key {key_press} in {locator}")
        locator = self._get_locator(locator)
        self.focus_element(locator)
        locator.press(key_press, delay=1500)
        return locator

    def verify_text_visible(self, text: str, parent_selector: str = None, is_exact: bool = False ):
        self.logger.info(f"Verifying text visible: '{text}' (Parent: {parent_selector})")

        root = self.page.locator(parent_selector) if parent_selector else self.page
        locator = root.get_by_text(text, exact=is_exact)

        expect(locator).to_be_visible(timeout=5000)

    def verify_element_visible(self, locator: str | Locator):
        self.logger.info(f"Verifying element visible: '{locator}'")
        expect(self._get_locator(locator)).to_be_visible()

    def verify_element_not_visible(self, locator: str | Locator):
        self.logger.info(f"Verifying element not visible: '{locator}'")
        expect(self._get_locator(locator)).not_to_be_visible()

    def verify_element_attribute(self, locator: str | Locator, attr_name: str, expected_attr_value: str):
        self.logger.info(f"Verifying attribute '{attr_name}' = '{expected_attr_value}'")
        actual_value = self._get_locator(locator).get_attribute(attr_name)
        assert expected_attr_value in actual_value, f"Expected '{expected_attr_value}' in '{actual_value}'"

    def verify_element_value(self, locator: str | Locator, expected_value: str):
        pattern = re.compile(rf".*{re.escape(expected_value)}.*", re.IGNORECASE)
        self.logger.info(f"Verifying element value: '{expected_value}'")
        expect(self._get_locator(locator)).to_have_value(pattern)

    def upload_file(self, locator: str | Locator, file_name: str, file_type: str):
        self.logger.info(f"Uploading file '{file_name}'")
        file_path = Path(__file__).resolve().parents[2] / "test_datas" / f"{file_name}.{file_type}"
        self._get_locator(locator).set_input_files(str(file_path))
        self.verify_element_value(locator, file_name)
