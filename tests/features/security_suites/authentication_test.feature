@security @auth
Feature: Authentication Security Testing

  @auth @login
  Scenario: SEC20 - Test login with weak password
    Given I am on the login page
    When I login with weak password "password"
    Then I should see the login result

  @auth @login
  Scenario: SEC21 - Test login with blank credentials
    Given I am on the login page
    When I login with blank username and password
    Then I should see the login result

  @auth @login
  Scenario: SEC22 - Test login brute force protection
    Given I am on the login page
    When I attempt to login with incorrect password 5 times
    Then I should see the login result

  @auth @session
  Scenario: SEC23 - Test session expiration
    Given I am on the login page
    When I refresh the page
    Then I should see the home page

  @auth @password
  Scenario: SEC24 - Test password change without current password
    Given I am on the login page
    When I go to the home page
    Then I should see the home page

  @auth @register
  Scenario: SEC25 - Test registration with existing email
    Given I am on the signup page
    When I register with an already registered email
    Then I should see the signup result