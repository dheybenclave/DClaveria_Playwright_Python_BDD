@api
Feature: Product API Validation

  @api @TC3 
  Scenario: Get all products list and verify response structure
    When I send a "GET" request to "/api/productsList"
    Then the API response status code should be 200
    And the response should contain a list of products
    And the API response time should be under 5000 ms
