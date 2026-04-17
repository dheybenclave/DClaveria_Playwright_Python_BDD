# Created by dheyb at 3/5/2026


Feature: User Login Validation

  @login @regression
  Scenario Outline: Login with credentials
    Given I navigate to <page>
    When I enter credentials using the <user_role> role
    Then I should expect the <result_message> message

    @positive_testing @TC1
    Examples:
      | page   | user_role | result_message |
      | /login | admin     | Logout         |

    @negative_testing @TC2
    Examples:
      | page   | user_role     | result_message                       |
      | /login | invalid_admin | Your email or password is incorrect! |


