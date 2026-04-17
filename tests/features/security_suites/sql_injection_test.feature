@security @sql_injection
Feature: SQL Injection Security Testing

  Background:
    Given I am on the login page

  @sql_injection @login_form
  Scenario: SEC01 - Test SQL injection on login form username field
    When I enter username with SQL injection payload "' OR '1'='1"
    And I enter any password
    And I click the login button
    Then the application should not expose database errors
    And the application should not allow unauthorized access

  @sql_injection @login_form
  Scenario: SEC02 - Test SQL injection on login form password field
    When I enter username "testuser"
    And I enter password with SQL injection payload "' OR '1'='1"
    And I click the login button
    Then the application should not expose database errors

  @sql_injection @search
  Scenario: SEC03 - Test SQL injection in search field
    Given I am on the products page
    When I search for products with SQL injection payload "' UNION SELECT NULL--"
    Then the application should not expose database errors

  @sql_injection @register
  Scenario: SEC04 - Test SQL injection in registration form
    Given I am on the signup page
    When I register with SQL injection payload in name field "' OR '1'='1"
    Then the application should handle the input safely

  @sql_injection @contact
  Scenario: SEC05 - Test SQL injection in contact form
    Given I am on the contact us page
    When I submit contact form with SQL injection payload "' OR '1'='1"
    Then the application should handle the input safely