import time
from pathlib import Path

from playwright.sync_api import sync_playwright
from pytest_bdd import when, parsers, scenarios

from utils.config import Config


@when(parsers.parse("I enter credentials using the {user_role} role"))
def enter_credentials_using_role(pages, user_role):
    pages.login_page.login_credentials(role=user_role)

@when(parsers.parse('I request api_suites "{endpoint}" via "{method}"'), target_fixture="api_res")
def api_step(pages, method, endpoint):
    start = time.perf_counter()
    with sync_playwright() as playwright:
        api_context = playwright.request.new_context(base_url=Config.BASE_URL)
        try:
            res = api_context.fetch(endpoint, method=method)
            res.perf_time = (time.perf_counter() - start) * 1000
            return res
        finally:
            api_context.dispose()
