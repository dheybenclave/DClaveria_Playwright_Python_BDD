Feature: End to End Testing of a new user that can place an order from start to beginning

  @e2e @TC6 
  Scenario Outline: Validate and Verify newly created user to place an order with specific order
    Given I navigate to <page>
    When I create a new user using the <user_data_id>
    Then I should expect the Congratulations! Your new account has been successfully created! message
    And I enter credentials using the newly created user
    When I search a product using the following category filter <filters>
    And I select product index <product_index> to view
    And I Add to cart with a quantity value of <quantity>
    When I navigate to cart
    And I click button "Proceed To Checkout"
    Then I validate and verify the address using the user details <user_data_id>
    Then I validate and verify the following order:
      | description   | price   | quantity   | total   |
      | <description> | <price> | <quantity> | <total> |
    Then I click button "Place Order"
    When I provide payment information using the card information id <card_info_id>
    Then I click button "Pay and Confirm Order"
    Then I should expect the Order Placed! message
    Then I should expect the Congratulations! Your order has been confirmed! message
    Then I validate and verify the generated invoice receipt


    @positive_testing @TC3
    Examples:
      | page   | user_data_id | filters     | product_index | description                   | price   | quantity | total    | card_info_id |
      | /login | 1            | Men,Tshirts | 4             | Pure Cotton Neon Green Tshirt | Rs. 850 | 2        | Rs. 1700 | 1            |


  @e2e @TC7
  Scenario Outline: Validate and Verify newly created user to place an order with multiple orders
    Given I navigate to <page>
    When I create a new user using the <user_data_id>
    Then I should expect the Congratulations! Your new account has been successfully created! message
    And I enter credentials using the newly created user
    When I search a product using the following category filter <filters>
    And I Add to cart by product index 1,5,3
    When I navigate to cart
    And I click button "Proceed To Checkout"
    Then I validate and verify the address using the user details <user_data_id>
    Then I validate and verify the following order:
      | description                      | price   | quantity | total   |
      | Sleeves Printed Top - White      | Rs. 499 | 1        | Rs. 499 |
      | Printed Off Shoulder Top - White | Rs. 315 | 1        | Rs. 315 |
      | Frozen Tops For Kids             | Rs. 278 | 1        | Rs. 278 |
    And I click button "Place Order"
    When I provide payment information using the card information id <card_info_id>
    And I click button "Pay and Confirm Order"
    Then I should expect the Order Placed! message
    Then I should expect the Congratulations! Your order has been confirmed! message
    Then I validate and verify the generated invoice receipt

    @positive_testing @TC3
    Examples:
      | page   | user_data_id | filters             | card_info_id |
      | /login | 1            | Kids, Tops & Shirts | 1            |

