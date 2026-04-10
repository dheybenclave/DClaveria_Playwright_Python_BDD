# Created by dheyb at 4/10/2026
Feature: API Testing for Automation Exercise

  @api @TC1
  Scenario: Get All Products List
    When I send a "GET" request to "/api/productsList"
    Then the API response status code should be 200
    And the response should contain a list of products

  @api @TC2
  Scenario: POST To All Products List (should fail)
    When I send a "POST" request to "/api/productsList"
    Then the API response status code should be 405

  @api @TC3
  Scenario: Get All Brands List
    When I send a "GET" request to "/api/brandsList"
    Then the API response status code should be 200
    And the response should contain a list of brands