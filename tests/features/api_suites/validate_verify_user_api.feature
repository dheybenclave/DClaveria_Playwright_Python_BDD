@api @user_api @TC101
Feature: User Account API Testing

  Background:
    Given the API base URL is configured

  @positive_testing @create_account
  Scenario: TC101 - Create new user account with valid data
    When I send a "POST" request to "/api/createAccount" with valid user data
    Then the response status code should be 201
    And the response should contain "message" indicating success

  @negative_testing @create_account
  Scenario: TC102 - Create account with existing email should fail
    When I send a "POST" request to "/api/createAccount" with duplicate email
    Then the response status code should be 400
    And the response should indicate the email already exists

  @positive_testing @login
  Scenario: TC103 - Login with valid credentials
    Given a user account exists in the system
    When I send a "POST" request to "/api/verifyLogin" with valid credentials
    Then the response status code should be 200
    And the response should contain a success message

  @negative_testing @login
  Scenario: TC104 - Login with invalid password
    Given a user account exists in the system
    When I send a "POST" request to "/api/verifyLogin" with wrong password
    Then the response status code should be 404
    And the response should indicate invalid credentials

  @negative_testing @login
  Scenario: TC105 - Login with non-existent email
    When I send a "POST" request to "/api/verifyLogin" with non-existent email
    Then the response status code should be 404
    And the response should indicate user not found

  @positive_testing @get_user
  Scenario: TC106 - Get user details by email
    Given a user account exists in the system
    When I send a "GET" request to "/api/getUserDetailByEmail" with the user's email
    Then the response status code should be 200
    And the response should contain the user's name and email

  @negative_testing @get_user
  Scenario: TC107 - Get user details with invalid email
    When I send a "GET" request to "/api/getUserDetailByEmail" with invalid email
    Then the response status code should be 404

  @positive_testing @update_account
  Scenario: TC108 - Update user account information
    Given a user account exists in the system
    When I send a "PUT" request to "/api/updateAccount" with new user data
    Then the response status code should be 200
    And the response should indicate successful update

  @negative_testing @update_account
  Scenario: TC109 - Update account with invalid credentials
    When I send a "PUT" request to "/api/updateAccount" with wrong password
    Then the response status code should be 404

  @positive_testing @delete_account
  Scenario: TC110 - Delete user account
    Given a user account exists in the system
    When I send a "DELETE" request to "/api/deleteAccount" with valid credentials
    Then the response status code should be 200
    And the response should indicate account deleted successfully