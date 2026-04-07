import os
from pathlib import Path

import pytest
from pytest_bdd import scenarios

# 1. Explicitly import API step modules so decorators are registered
from tests.step_definitions.api import test_api_get_all_product_list  # noqa: F401

# 2. Load all feature scenarios (UI + API)
FEATURES_DIR = Path(__file__).resolve().parent.parent / "features"
scenarios(str(FEATURES_DIR))


@pytest.fixture(scope="session", autouse=True)
def teardown_context():
    from utils.test_state import context

    context.cleanup()
    yield
