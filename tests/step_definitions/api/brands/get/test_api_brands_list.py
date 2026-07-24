# Brands API step definitions - uses shared steps from products
from pytest_bdd import then


@then("the response should contain brands data")
def verify_brands_data(api_response_data: dict) -> None:
    """Verify response contains brands data"""
    json_data = api_response_data["json"]
    assert "brands" in json_data, "Key 'brands' missing from response"
    assert isinstance(json_data["brands"], list), "Brands should be a list"
