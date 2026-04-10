import logging
import os

from playwright.sync_api import Page, Locator

from src.pages.base_page import UIBasePage
from utils.test_state import context


class PaymentPage(UIBasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.pid = os.getpid()

    @property
    def txt_name_card(self) -> Locator:
        return self.page.locator("[name=name_on_card]")

    @property
    def txt_card_number(self) -> Locator:
        return self.page.locator("[name=card_number]")

    @property
    def txt_cvc(self) -> Locator:
        return self.page.locator("[name=cvc]")

    @property
    def txt_expiry_month(self) -> Locator:
        return self.page.locator("[name=expiry_month]")

    @property
    def txt_expiry_year(self) -> Locator:
        return self.page.locator("[name=expiry_year]")

    def validate_card_info(self, card_info_id):
        self.logger.info(f"Validate Card Information using the Card ID :{card_info_id} from JSON")

        test_data = self.utils.get_json_data("card_information.json", card_info_id)
        expiry_month = str(test_data.get("expiration")).split("/")[0].strip()
        expiry_year = str(test_data.get("expiration")).split("/")[1].strip()

        self.common_page.enter_text(self.txt_name_card, context.get_strict("full_name"))
        self.common_page.enter_text(self.txt_card_number, test_data["card_number"])
        self.common_page.enter_text(self.txt_cvc, test_data["cvc"])
        self.common_page.enter_text(self.txt_expiry_month, expiry_month)
        self.common_page.enter_text(self.txt_expiry_year, expiry_year)

        self.logger.info("Card Details Entered Successfully")

    def validate_verify_invoice_receipt(self):
        self.logger.info("Validate Generated Invoice Receipt")

        results_dir = os.path.join(os.getcwd(), "test-results/test_state")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        with self.page.expect_download() as download_info:
            self.page.get_by_text("Download Invoice").click()

        download = download_info.value

        file_name = f"{self.pid}_{download.suggested_filename}"
        file_path = os.path.join(results_dir, file_name)

        download.save_as(file_path)

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            self.logger.info(f"Invoice successfully saved to: {file_path}")
        else:
            raise FileNotFoundError(f"Invoice download failed or file is empty at {file_path}")


        self.logger.info("Validate Generated Invoice Receipt Successfully")

        self.verify_invoice_content(file_path)

        return file_path


    def verify_invoice_content(self, file_path):
        self.logger.info(f"Verify Generated Invoice Receipt Content of: {file_path}")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PID {self.pid} could not find its invoice at {file_path}")

        with open(file_path, 'r') as f:
            content = f.read().strip()

        self.logger.debug(f"Actual Invoice Text: '{content}'")

        expected_name = context.get_strict("full_name")
        expected_amount = context.get_strict("total_amount")

        assert expected_name in content, f"Expected name '{expected_name}' not found in invoice receipt!"
        self.logger.info(f"Successfully verified Name: '{expected_name}' exists in the invoice.")

        assert f"total purchase amount is {expected_amount}" in content, "Invoice amount was not 0 as expected for this test in invoice receipt."
        self.logger.info(f"Successfully verified Amount: '{expected_amount}' matches the invoice receipt.")

        self.logger.info(f"Verify Generated Invoice Receipt Successfully! : {file_path} ")

