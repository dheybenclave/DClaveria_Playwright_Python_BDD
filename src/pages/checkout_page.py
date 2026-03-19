import logging

from playwright.sync_api import Page, Locator, expect

from src.pages.base_page import BasePage
from utils.test_state import context


class CheckoutPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def table_cart(self) -> Locator:
        return self.page.locator("#cart_info")

    @property
    def table_cart_rows(self) -> Locator:
        return self.page.locator("#cart_info tbody tr")

    def get_row_by_index(self, row_index: int) -> Locator:
        return self.table_cart_rows.nth(row_index - 1)

    @property
    def lbl_cart_products(self) -> Locator:
        return self.page.locator("td.cart_product")

    @property
    def lbl_cart_descriptions(self) -> Locator:
        return self.page.locator("td.cart_description a")

    @property
    def lbl_cart_prices(self) -> Locator:
        return self.page.locator("td.cart_price p")

    @property
    def lbl_cart_quantities(self) -> Locator:
        return self.page.locator("td.cart_quantity button")

    @property
    def lbl_cart_total(self) -> Locator:
        return self.page.locator("td.cart_total p")

    @property
    def lbl_cart_total_amount(self) -> Locator:
        return self.page.locator("td p.cart_total_price").last

    def validate_verify_address(self, user_id_json):
        self.logger.info("Validate And verify Address of the user/account")

        test_data = self.utils.get_json_data("register_user_data.json", user_id_json)

        full_name = f"{test_data["title"]}. {test_data["firstname"]} {test_data['lastname']}"
        address_city_state_zip = f" {test_data["city"]} {test_data["state"]} {test_data['zipcode']}"

        address_list = [
            full_name,
            test_data["company"],
            test_data["address1"],
            test_data["address2"],
            address_city_state_zip,
            test_data["country"],
            test_data["mobile_number"],
        ]

        for address in address_list:
            self.logger.info(f"Verify Address of the user/account : {address} ")
            self.common_page.verify_text_visible(text=address, is_exact=True, parent_selector="#address_delivery")

    def validate_verify_orders(self, orders: dict | list[dict]):
        self.logger.info("Validating and Verifying Orders ")

        expected_list = [orders] if isinstance(orders, dict) else orders
        self.logger.info(f"Expected Product Details: {expected_list}")

        expect(self.table_cart).to_be_visible()

        actual_ui_details = self.get_products_details()
        self.logger.info(f"Actual UI Product Details: {actual_ui_details}")

        for expected in expected_list:
            match = next((
                item for item in actual_ui_details
                if item["description"].strip() == expected.get("description").strip()), None)

            if match:
                self.logger.info(f"Match Found for: {match['description']}")

                assert match["description"] == expected.get(
                    "description"), f"Description mismatch for {match['Description']}"
                assert match["price"] == expected.get("price"), f"Price mismatch for {match['Description']}"
                assert match["quantity"] == str(expected.get("quantity")), f"Qty mismatch for {match['Description']}"
                assert match["total"] == expected.get("total"), f"Total mismatch for {match['Description']}"
            else:
                raise AssertionError(
                    f"Product '{expected.get('description')}' was expected but not found in the Cart UI!")

        assert len(actual_ui_details) == len(expected_list), \
            f"Cart count mismatch! UI has {len(actual_ui_details)}, but expected {len(expected_list)}"

        self.get_total_amount()

    def get_products_details(self) -> list[dict]:
        self.logger.info("Get All Products Details")

        self.table_cart_rows.first.wait_for(state="visible", timeout=10000)

        row_count = self.table_cart_rows.count()
        self.logger.info(f"Found {row_count} total rows (including footer)")

        get_all_product_data = []

        for i in range(1, row_count):
            self.logger.info(f"Scraping product row index: {i}")

            row_data = self.get_products_details_by_row(i)
            get_all_product_data.append(row_data)

        return get_all_product_data

    def get_products_details_by_row(self, row_index: int = 1) -> dict:
        self.logger.info(f"Get Table Cart Product by Row: {row_index}")

        row = self.get_row_by_index(row_index)

        return {
            "description": row.locator(self.lbl_cart_descriptions).inner_text().strip(),
            "price": row.locator(self.lbl_cart_prices).inner_text().strip(),
            "quantity": row.locator(self.lbl_cart_quantities).inner_text().strip(),
            "total": row.locator(self.lbl_cart_total).inner_text().strip()
        }

    def get_total_amount(self) -> float:
        self.logger.info("Getting Total Amount from UI")

        raw_text = self.lbl_cart_total_amount.inner_text().strip()

        clean_text = raw_text.replace("Rs.", "").replace(",", "").strip()

        try:
            total = int(clean_text)
            self.logger.debug(f"Parsed Total Amount: {total}")
            context.set("total_amount", total)
            return total
        except ValueError:
            self.logger.error(f"Could not convert '{raw_text}' to a number.")
            context.set("total_amount", 0)
            return 0
