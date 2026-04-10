import time

from pytest_bdd import when, then, parsers


# Using target_fixture to pass data between steps (Performance, json, Response)
@when(parsers.parse('I send a "{method}" request to "{endpoint}"'), target_fixture="api_response_data")
def send_request(pages, method, endpoint):
    endpoint_key = endpoint.strip().lower()
    if endpoint_key == "/api/productslist":
        api_client = pages.api.all_products
        if method.upper() == "GET":
            response_call = api_client.get_all_products
        elif method.upper() == "POST":
            response_call = pages.api.post_to_all_products_list.post_to_products_list
        else:
            raise AssertionError(f"Unsupported method '{method}' for endpoint '{endpoint}'")
    elif endpoint_key == "/api/brandslist":
        api_client = pages.api.get_all_brands_list
        response_call = api_client.get_all_brands
    else:
        raise AssertionError(f"Unsupported endpoint in this step file: {endpoint}")

    start_time = time.perf_counter()
    response = response_call()
    duration_ms = round((time.perf_counter() - start_time) * 1000)
    response_json = response.json()

    # Store in global context
    from src.context import test_context
    test_context.last_response = {
        "response": response,
        "json": response_json,
        "duration": duration_ms,
        "endpoint": endpoint,
        "method": method
    }

    return test_context.last_response


@then(parsers.parse('the API response status code should be {status:d}'))
def verify_status(pages, api_response_data, status):
    response_json = api_response_data["json"]
    response = api_response_data["response"]
    if "products" in response_json:
        pages.api.all_products.verify_response_status_code(response, status)
        return
    if "brands" in response_json:
        pages.api.get_all_brands_list.verify_response_status_code(response, status)
        return
    if "message" in response_json:
        response_code = response_json.get("responseCode", response.status)
        assert response_code == status, f"Expected responseCode {status}, but got {response_code}"
        return
    raise AssertionError("Unknown response payload; cannot verify status.")


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
    pages.api.all_products.validate_product_structure(
        api_response_data["json"],
        required_keys
    )


@then(parsers.parse('the API response time should be under {limit:d} ms'))
def verify_performance(pages, api_response_data, limit):
    get_duration = api_response_data["duration"]
    response_json = api_response_data["json"]
    if "products" in response_json:
        pages.api.all_products.verify_performance_of_response(get_duration, limit)
        return
    if "brands" in response_json:
        pages.api.get_all_brands_list.verify_performance_of_response(get_duration, limit)
        return
    raise AssertionError("Unknown response payload; cannot verify performance.")


@then("the response should contain a list of brands")
def verify_brand_list_exists(api_response_data):
    json_data = api_response_data["json"]
    assert "brands" in json_data, "Key 'brands' missing from response"
    assert len(json_data["brands"]) > 0, "Brands list is empty"
