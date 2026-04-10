from pytest_bdd import when, parsers, given, then


@when(parsers.parse("I enter credentials using the {user_role} role"))
def enter_credentials_using_role(pages, user_role):
    pages.ui.login_page.login_credentials_by_role(role=user_role)

@then("I enter credentials using the newly created user")
def enter_credential_with_created_user(pages):
    pages.ui.login_page.login_credential_with_created_user()


