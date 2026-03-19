from pytest_bdd import parsers, then, when



@then(parsers.parse("I validate and verify the address using the user details {user_data_id}"))
def validate_address(pages, user_data_id):
   pages.ui.checkout_page.validate_verify_address(user_data_id)

@then("I validate and verify the following order:")
def validate_order(pages, datatable):
    headers = datatable[0]
    data_rows = [dict(zip(headers, row)) for row in datatable[1:]]

    pages.ui.checkout_page.validate_verify_orders(data_rows)


