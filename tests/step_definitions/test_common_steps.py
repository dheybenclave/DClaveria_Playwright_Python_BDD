from typing import Any

from pytest_bdd import parsers, given, then


@given(parsers.parse('I navigate to {page}'))
def navigate_to_page(pages: Any, page: str) -> None:
    """Navigates using the unified dynamic 'pages' factory."""
    pages.ui.common_page.open_browser(page.strip())


@then(parsers.parse("I should expect the {result_text_message} message"))
def verify_login_message(pages, result_text_message: str) -> None:
    """Verifies visibility of a UI message, ignoring 'N/A' placeholders."""
    # Using a set for O(1) lookup efficiency
    ignore_set = {"N/A", "NA", "NONE", ""}

    if not result_text_message or result_text_message.strip().upper() in ignore_set:
        return

    pages.ui.common_page.verify_text_visible(result_text_message)

