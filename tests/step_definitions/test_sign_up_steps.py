from pytest_bdd import parsers, then, when


@then(parsers.parse("I create a new user using the {test_data_id}"))
def create_a_new_user(pages, test_data_id):
    pages.ui.sign_up_page.create_new_user_by_sign_up(test_data_id)


@when(parsers.parse("I create a new user using the {test_data_id}"))
def create_a_new_user_when(pages, test_data_id):
    pages.ui.sign_up_page.create_new_user_by_sign_up(test_data_id)
