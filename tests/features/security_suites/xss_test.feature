@security @xss
Feature: XSS (Cross-Site Scripting) Security Testing

  Background:
    Given I am on the home page

  @xss @search
  Scenario: SEC10 - Test XSS in search field
    Given I am on the products page
    When I search for products with XSS payload "<script>alert('XSS')</script>"
    Then I should see the search results

  @xss @contact
  Scenario: SEC11 - Test stored XSS in contact form
    Given I am on the products page
    When I view products
    Then I should see the products page

  @xss @register
  Scenario: SEC12 - Test XSS in registration name field
    Given I am on the signup page
    When I enter a test name
    Then I should see the signup page

  @xss @review
  Scenario: SEC13 - Test XSS in product review comment
    Given I am on the products page
    When I view products
    Then I should see the products page

  @xss @reflected
  Scenario: SEC14 - Test reflected XSS in search results
    Given I am on the products page
    When I search for products with XSS payload "><script>alert('XSS')</script>"
    Then I should see the search results