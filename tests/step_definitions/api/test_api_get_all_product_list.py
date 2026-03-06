import time

from pytest_bdd import when, then, parsers


# Using target_fixture to pass data between steps (Performance, JSON, Response)
@when(parsers.parse('I send a "{method}" request to "{endpoint}"'), target_fixture="api_response_data")
def send_request(pages, method, endpoint):
    # Dynamically resolve the API module (get_all_product_list.py)
    api_client = pages.api.get_all_product_list

    start_time = time.perf_counter()
    response = api_client.get_all_products()
    duration_ms = round((time.perf_counter() - start_time) * 1000)
    response_json = response.json()

    return {
        "response": response,
        "json": response_json,
        "duration": duration_ms
    }


@then(parsers.parse('the API response status code should be {status:d}'))
def verify_status(pages, api_response_data, status):
    # Accessing the specific validation logic in the dynamically loaded API class
    pages.api.get_all_product_list.verify_response_status_code(
        api_response_data["response"],
        status
    )


@then("the response should contain a list of products")
def verify_list_exists(api_response_data):
    # Direct validation of the shared fixture data
    json_data = api_response_data["json"]
    assert "products" in json_data, "Key 'products' missing from response"
    assert len(json_data["products"]) > 0, "Product list is empty"


@then(parsers.parse('every product should have the following parameter:'))
def verify_product_schema_from_table(datatable, pages, api_response_data):
    # Extract keys from Gherkin table: | id | | name | etc.
    required_keys = [row[0].strip() for row in datatable[1:] if row and row[0].strip()]

    # Use the logger inherited by any page object (e.g., ui.common_page)
    pages.logger.debug(f"Validating Schema | Required Keys: {required_keys}")

    # Call the validation method in your API page object
    pages.api.get_all_product_list.validate_product_structure(
        api_response_data["json"],
        required_keys
    )


@then(parsers.parse('the API response time should be under {limit:d} ms'))
def verify_performance(pages, api_response_data, limit):
    # Logic remains inside the specific API class for specialized performance thresholds
    get_duration = api_response_data["duration"]
    pages.api.get_all_product_list.verify_performance_of_response(get_duration, limit)
