# Sanity Test Suite - Smoke Tests for Core Application Flows
# Purpose: Quick validation that critical paths are functional before full regression
# Created: 2026-04-20
# Tags: @sanity @smoke @quick

Feature: Application Sanity Testing

  Background:
    Given the application is up and running

  @sanity @ui @TC200
  Scenario: Home page should load successfully
    Given I navigate to /
    Then I should expect the Signup / Login message

  @sanity @ui @login @TC201
  Scenario: Valid user can login successfully
    Given I navigate to /login
    When I enter credentials using the admin role
    Then I should expect the Logout message

  @sanity @ui @login @TC202
  Scenario: Logout functionality works correctly
    Given I navigate to /login
    When I enter credentials using the admin role
    And I click button "Logout"
    Then I should expect the Signup / Login message

  @sanity @ui @products @TC203
  Scenario: Products page should display products
    Given I navigate to /products
    Then I should expect the ALL PRODUCTS message

  @sanity @ui @navigation @TC204
  Scenario: Navigation between main pages works
    Given I navigate to /
    When I navigate using text "Products"
    Then I should expect the ALL PRODUCTS message
    When I navigate using text "Home"
    Then I should expect the Signup / Login message
