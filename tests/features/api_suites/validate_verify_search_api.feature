@api @search_api @TC301
Feature: Search Product API Testing

  Background:
    Given the API base URL is configured

  @positive_testing @search
  Scenario: TC301 - Search for products with valid query
    When I send a "POST" request to "/api/searchProduct" with search query "shirt"
    Then the response status code should be 200
    And the response should contain a list of products

  @positive_testing @search
  Scenario: TC302 - Search for products with partial match
    When I send a "POST" request to "/api/searchProduct" with search query "dress"
    Then the response status code should be 200
    And the response should contain matching products

  @positive_testing @search
  Scenario: TC303 - Search returns empty results for non-existent product
    When I send a "POST" request to "/api/searchProduct" with search query "xyznonexistent123"
    Then the response status code should be 200
    And the response should indicate no products found

  @positive_testing @search
  Scenario: TC304 - Search with special characters
    When I send a "POST" request to "/api/searchProduct" with search query "blue%shirt"
    Then the response status code should be 200