@api @regression
Feature: Brands API Validation

  @api @TC4
  Scenario: Get all brands list and verify response structure
    When I send a "GET" request to "/api/brandsList"
    Then the API response status code should be 200
    And the response should contain a list of brands
    And the API response time should be under 5000 ms
