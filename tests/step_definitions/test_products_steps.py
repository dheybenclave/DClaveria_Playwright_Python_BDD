from pytest_bdd import parsers, when


@when(parsers.parse("I search a product using the following category filter {filters}"))
def search_product_using_filter(pages, filters):
    pages.ui.products_page.search_product_filter_by_category(filters.split(","))


@when(parsers.parse("I select product index {product_index} to view"))
def select_product_using_index(pages, product_index):
    pages.ui.products_page.select_product_index(product_index)


@when(parsers.parse("I Add to cart with a quantity value of {quantity}"))
def add_to_cart_with_quantity(pages, quantity):
    for quantity in range(1, int(quantity) + 1):
        pages.ui.products_page.add_to_cart()


@when(parsers.parse("I Add to cart by product index {product_indices}"))
def add_to_cart_by_index(pages, product_indices):
    index_list = [int(x.strip()) for x in product_indices.split(",")]

    for index in index_list:
        pages.ui.products_page.add_to_cart_by_index(index)
