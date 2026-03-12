from pytest_bdd import parsers, then, when, given


@when(parsers.parse("I search a product using the following filter [{filters}]"))
def search_product_using_filter(pages, filters: list[str]):
    return None


@when(parsers.parse("I select product index {product_index} to view"))
def select_product_index(pages, product_index):
    return None


@when(parsers.parse("I Add to cart with a quantity value of {quantity}"))
def add_to_cart_with_quantity(pages, quantity):
    return None


@then(parsers.parse("I validate and verify the address using the user details {user_data_id}"))
def validate_address(pages, user_data_id):
    return None


@then("I validate and verify the following order:")
def validate_order(pages, datatable):
    return None


@when("I provide payment information using the following:")
def provide_payment_info(pages, metadata):
    return None
