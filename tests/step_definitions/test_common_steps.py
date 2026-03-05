from pathlib import Path

from playwright.sync_api import Page
from pytest_bdd import parsers, given, then, scenarios

from src.pages.common_page import CommonPage
from tests.step_definitions.test_login_steps import * #all future test steps should import in here

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
scenarios(str(FEATURES_DIR))

@given(parsers.parse("I navigate to {page_path}"))
def navigate_to_page(playwright_page: Page, page_path):
    playwright_page.page = CommonPage(playwright_page)
    playwright_page.page.open_browser(page_path.strip())
    return playwright_page

@then(parsers.parse("I should expect the {result_text_message} message"))
def verify_login_message(pages, result_text_message):
    if result_text_message.strip().upper() in {"N/A", "NA", "NONE", ""}:
        return
    pages.common_page.verify_text_visible(result_text_message)

@then(parsers.parse('the response time should be under {ms:d} ms'))
def check_perf(api_res, ms):
    assert api_res.perf_time < ms, f"Slow response: {api_res.perf_time}ms"
