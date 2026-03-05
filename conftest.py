import os
import shutil
from datetime import datetime
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from src.pages.base_page import BasePage

load_dotenv()


def _safe_path_part(value: str) -> str:
    invalid = '<>:"/\\|?*[]'
    safe = "".join("_" if ch in invalid else ch for ch in value)
    return safe.strip() or "unnamed_test"


@pytest.fixture
def playwright_page(request):
    test_name = _safe_path_part(request.node.name)
    root_dir = request.config.rootpath

    video_path = os.path.join(root_dir, "test-results", "videos", str(test_name))
    screenshot_path = os.path.join(root_dir, "test-results", "screenshots", str(test_name))

    # Create directories
    os.makedirs(video_path, exist_ok=True)
    os.makedirs(screenshot_path, exist_ok=True)

    # Boolean flag for easier reading
    save_recorded_video = os.environ.get("RECORD_VIDEO", "false").lower() == "true"
    headless_env = os.environ.get("HEADLESS", "true").lower() == "true"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless_env)

        # Always enable recording if the ENV is true so Playwright captures the session
        context = browser.new_context(
            record_video_dir=video_path if save_recorded_video else None
        )
        # Keep a realistic timeout for external site/UI operations.
        context.set_default_timeout(15000)
        page = context.new_page()

        # Block specific ad domains and non-essential media
        def block_ads(route):
            url = route.request.url.lower()
            resource_type = route.request.resource_type

            # Add common ad keywords or domains here
            ad_keywords = ["googleads", "ads-twitter", "facebook"]

            # if any(keyword in url for keyword in ad_keywords) or resource_type in ["image", "media", "font"]:
            if any(keyword in url for keyword in ad_keywords):
                return route.abort()
            return route.continue_()

        page.route("**/*", block_ads)

        try:
            yield page
        finally:
            # Check if the test actually failed (requires the hook pytest_run_makereport)
            # We check 'rep_call' specifically for test body failures
            result_outcome = getattr(request.node, "rep_call", None)
            test_failed = result_outcome and result_outcome.failed

            # If test passed, no screenshot and delete folder not required (empty)
            if not test_failed and os.path.exists(screenshot_path):
                shutil.rmtree(screenshot_path)

            # If test failed, take screenshot
            if test_failed:
                now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                page.screenshot(path=f"{screenshot_path}/{test_name}_{now}.jpg")

            # VERY IMPORTANT: close context to finalize video
            context.close()

            # If test passed OR recording was disabled, delete the video folder
            if (not test_failed or not save_recorded_video) and os.path.exists(video_path):
                shutil.rmtree(video_path)

            # Now it's safe to close browser
            browser.close()


@pytest.fixture
def pages(playwright_page) -> BasePage:
    """Fixture for page object model"""
    return BasePage(playwright_page)


def pytest_configure(config):
    report_dir = Path(config.rootpath) / "test-results" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    # Workers do not create the final HTML report.
    if hasattr(config, "workerinput"):
        return

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = str(report_dir / f"report_{now}.html")
    config.option.self_contained_html = True


def pytest_sessionstart(session):
    htmlpath = getattr(session.config.option, "htmlpath", None)
    if htmlpath:
        Path(htmlpath).parent.mkdir(parents=True, exist_ok=True)


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    htmlpath = getattr(session.config.option, "htmlpath", None)
    if htmlpath:
        Path(htmlpath).parent.mkdir(parents=True, exist_ok=True)


def log_api_details(response):
    allure.attach(
        body=str(response.url),
        name="api_suites URL",
        attachment_type=allure.attachment_type.TEXT
    )
    allure.attach(
        body=str(response.json()),
        name="api_suites Response JSON",
        attachment_type=allure.attachment_type.JSON
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Set a report attribute for each phase of a call (setup, call, teardown)
    # This allows the fixture to check if the test failed
    setattr(item, "rep_" + rep.when, rep)
