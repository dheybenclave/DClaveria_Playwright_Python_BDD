# Created by dheyb at 3/5/2026
Feature: Sing Up new User Validation

  @signup @regression
  Scenario Outline: Sign Up a new user
    Given I navigate to <page>
    Then I create a new user using the <test_data_id>
    Then I should expect the <result_message> message

    @positive_testing @TC3
    Examples:
      | page   | test_data_id | result_message                                                   |
      | /login |            1 | Congratulations! Your new account has been successfully created! |

    @positive_testing @TC4
    Examples:
      | page   | test_data_id | result_message                                                   |
      | /login |            5 | Congratulations! Your new account has been successfully created! |

    @negative_testing @TC5
    Examples:
      | page   | test_data_id | result_message |
      | /login |           11 | INVALID_DATA   |
