Feature: validate_verify_place_order_item

  @e2e @TC6
  Scenario Outline: validate_verify_place_order_item
    Given I navigate to <page>
    When I create a new user using the <user_data_id>
    Then I should expect the Congratulations! Your new account has been successfully created! message
    And I enter credentials using the newly created user
#    When I search a product using the following filter [<filters>]
#    And I select product index <product_index> to view
#    And I Add to cart with a quantity value of <quantity>
#    Then I should expect the Your product has been added to cart. message
#    And I click button "Continue Shopping"
#    When I navigate to cart
#    Then I click button "Proceed To checkout"
#    Then I validate and verify the address using the user details <user_data_id>
#    Then I validate and verify the following order:
#      | Description   | Price   | Quantity   | Total   |
#      | <description> | <price> | <quantity> | <total> |
#    Then I click button "Place Order"
#    When I provide payment information using the following:
#      | Name on Card   | Card Number   | CVC   | Expiration   |
#      | <user_data_id> | <card_number> | <cvc> | <expiration> |
#    Then I click button "Pay and Confirm Order"
#    Then I should expect the Order Placed! message
#    Then I should expect the Congratulations! Your order has been confirmed! message

    @positive_testing @TC3
    Examples:
      | page   | user_data_id | filters         | product_index | description | price   | quantity | total    | card_number  | cvc | expiration |
      | /login | 1            | "Men","Tshirts" | 4             | Winter Top  | Rs. 600 | 2        | Rs. 1200 | 123512351235 | 123 | 03/30      |

