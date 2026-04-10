from pytest_bdd import parsers, when, then


@when(parsers.parse("I provide payment information using the card information id {card_info_id}"))
def validate_card_info(pages, card_info_id):
   pages.ui.payment_page.validate_card_info(card_info_id)


@then("I validate and verify the generated invoice receipt")
def validate_invoice_receipt(pages):
   pages.ui.payment_page.validate_verify_invoice_receipt()
