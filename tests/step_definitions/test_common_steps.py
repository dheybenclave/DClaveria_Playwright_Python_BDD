from pytest_bdd import parsers, given, then, when


@given(parsers.parse('I navigate to {page_url_or_text}'))
@when(parsers.parse('I navigate to {page_url_or_text}'))
def navigate_to_page(pages, page_url_or_text: str) -> None:
    """Navigates using the unified dynamic 'pages' factory."""

    if "/" in page_url_or_text:
        pages.ui.common_page.open_browser(page_url_or_text.strip())
    else:
        pages.ui.common_page.navigate_to_by_text(page_url_or_text)


@then(parsers.parse("I should expect the {result_text_message} message"))
def verify_result_message(pages, result_text_message: str) -> None:
    """Verifies visibility of a UI message, ignoring 'N/A' placeholders."""
    ignore_set = {"N/A", "NA", "NONE", "INVALID_DATA", ""}

    if not result_text_message or result_text_message.strip().upper() in ignore_set:
        return

    pages.ui.common_page.verify_text_visible(result_text_message)


@given(parsers.parse('I click button "{button_text}"'))
@then(parsers.parse('I click button "{button_text}"'))
def click_button_by_text(pages, button_text):
    pages.ui.common_page.click_element_by_text(button_text)
