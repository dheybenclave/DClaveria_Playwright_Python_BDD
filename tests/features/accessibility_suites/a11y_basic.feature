@a11y @axe @A11Y01
Feature: Basic Accessibility Testing

  Background:
    Given I am on the home page

  @axe @homepage
  Scenario: A11Y01 - Home page passes axe-core accessibility audit
    Then accessibility audit should pass with no critical violations

  @axe @homepage
  Scenario: A11Y02 - Home page should have no serious accessibility violations
    Then accessibility audit should pass with no serious violations

  @axe @homepage
  Scenario: A11Y03 - Home page should have proper ARIA landmarks
    Then the page should have main landmark
    And the page should have navigation landmark

  @axe @homepage
  Scenario: A11Y04 - Home page should have document title
    Then the page should have proper document title

  @axe @homepage
  Scenario: A11Y05 - Home page should have lang attribute
    Then the page should have lang attribute on html element