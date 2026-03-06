from pytest_bdd import when, parsers


@when(parsers.parse("I enter credentials using the {user_role} role"))
def enter_credentials_using_role(pages, user_role):
    pages.ui.login_page.login_credentials_by_role(role=user_role)


