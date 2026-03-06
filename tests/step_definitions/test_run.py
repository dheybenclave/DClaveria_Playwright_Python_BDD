from pathlib import Path
from pytest_bdd import scenarios

# 1. Explicitly import all step files so decorators are registered
# Because of 'pythonpath = .' in pytest.ini, these imports are now clean
# from tests.step_definitions import test_login_steps
# from tests.step_definitions import test_common_steps
# from tests.step_definitions.api import test_api_get_all_product_list

# 2. Load scenarios
FEATURES_DIR = Path(__file__).resolve().parent.parent / "features"
scenarios(str(FEATURES_DIR))