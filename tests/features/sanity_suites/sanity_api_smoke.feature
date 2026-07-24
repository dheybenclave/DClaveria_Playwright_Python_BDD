# Sanity Test Suite - API Smoke Tests
# Purpose: Validate core API endpoints are responsive and returning correct data
# Created: 2026-04-20
# Tags: @sanity @api @smoke

Feature: API Sanity Testing

  Background:
    Given the API base URL is configured

  @sanity @api @products @TC205
  Scenario: GET all products list API should return data
    When I send a "GET" request to "/api/productsList"
    Then the response status code should be 200
    And the response should contain products data

  @sanity @api @brands @TC206
  Scenario: GET all brands list API should return data
    When I send a "GET" request to "/api/brandsList"
    Then the response status code should be 200
    And the response should contain brands data

  @sanity @api @create_account @TC207
  Scenario: POST create account with valid data should succeed
    When I send a "POST" request to "/api/createAccount" with valid user data
    Then the response status code should be 201
    And the response should contain "message" indicating success

  @sanity @api @login @TC208
  Scenario: POST verifyLogin with valid credentials should succeed
    Given a user account exists in the system
    When I send a "POST" request to "/api/verifyLogin" with valid credentials
    Then the response status code should be 200
    And the response should contain a success message

  @sanity @api @search @TC209
  Scenario: POST search product should return results
    When I send a "POST" request to "/api/searchProduct" with search term "tshirt"
    Then the response status code should be 200
    And the response should contain search results
