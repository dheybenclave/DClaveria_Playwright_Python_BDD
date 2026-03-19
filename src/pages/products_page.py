import logging
from typing import List

from playwright.sync_api import Page, Locator

from src.pages.base_page import BasePage


class ProductsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def btn_view_products(self) -> Locator:
        return self.page.locator("div.features_items div.choose")

    @property
    def btn_add_to_cart(self) -> Locator:
        return self.page.locator("button.cart")

    def btn_add_to_cart_by_index(self, product_index=1) -> Locator:
        return self.page.locator("div.productinfo a.add-to-cart").nth(int(product_index) - 1)

    def nav_category(self, category: str, sub_category=None) -> Locator:

        if sub_category is None:
            return self.page.locator(f"div.category-products a[href='#{category}']")
        else:
            return self.page.locator(f"#{category}").get_by_text(sub_category.capitalize(), exact=False)

    def search_product_filter_by_category(self, categories_filter: List[str]):

        category_filter = categories_filter[0]
        sub_category_filter = categories_filter[1]

        self.logger.info(f"Search Product by Category: {category_filter} > Sub Category : {sub_category_filter}")

        self.common_page.navigate_to_by_text("Products")
        self.page.wait_for_load_state("networkidle")

        self.nav_category(category_filter).click()
        self.nav_category(category_filter, sub_category_filter).click()

        self.page.wait_for_load_state("networkidle")

        self.common_page.verify_text_visible(
            f"{category_filter.capitalize()} - {sub_category_filter.capitalize()} Products")

    def select_product_index(self, index_count_table_grid=1):

        self.logger.info(f"Select Product Index: {index_count_table_grid}")

        self.btn_view_products.nth(index_count_table_grid).click()
        self.page.wait_for_load_state("networkidle")

        self.common_page.verify_text_visible("Add to cart")

    def add_to_cart(self):
        self.logger.info(f"Add Product to cart")

        self.btn_add_to_cart.click()
        self.common_page.verify_text_visible("Your product has been added to cart.")
        self.common_page.click_element_by_text("Continue Shopping")
        self.page.wait_for_load_state("domcontentloaded")

    def add_to_cart_by_index(self, product_index: int = 1):
        self.logger.info(f"Add Product to cart")
        self.btn_add_to_cart_by_index(product_index).click()
        self.common_page.verify_text_visible("Your product has been added to cart.")
        self.common_page.click_element_by_text("Continue Shopping")
        self.page.wait_for_load_state("domcontentloaded")
