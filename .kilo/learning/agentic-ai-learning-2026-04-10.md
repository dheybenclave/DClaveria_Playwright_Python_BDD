# Agentic AI Self-Aware Learning Log

## Session: 2026-04-10

### Commands & Prompts Executed

| # | Command/Prompt | Purpose | Result |
|---|----------------|---------|--------|
| 1 | `pytest -n auto` | Run all tests in parallel | Found 3 failing tests (TC3 API tests + 1 sign up test) |
| 2 | `pytest -n 0 -m "TC3" --tb=long` | Debug TC3 API tests | Could not see full traceback due to allure blocking |
| 3 | Grep allure-results for error details | Find failure reasons | Found: `AttributeError: 'ApiBasePage' object has no attribute 'get_all_product_list'` |
| 4 | Read `src/pages/api/base_api.py` | Check API page class | Found property named `all_products` not `get_all_product_list` |
| 5 | Edit `test_api_products_list.py` - Fix method name | Fix broken method reference | Changed `pages.api.get_all_product_list` → `pages.api.all_products` |
| 6 | `pytest -n 0 -m "TC3"` | Verify TC3 fix | All TC3 tests now pass |
| 7 | `pytest -n auto` | Full regression run | 14 passed, 1 failed (pre-existing test data issue) |
| 8 | Grep allure-results for login-11-INVALID_DATA | Investigate remaining failure | Found: Country dropdown timeout - test data has "Florida" instead of valid country name |

### Key Learnings

#### 1. API Method Naming Issue
- **Problem**: Step definitions used wrong method name `get_all_product_list`
- **Root Cause**: Method was renamed to `all_products` in ApiBasePage but step definitions weren't updated
- **Fix**: Update step definitions to use `pages.api.all_products` instead

#### 2. Allure Plugin Blocking Test Output
- **Problem**: pytest timed out waiting for allure report generation after every run
- **Root Cause**: allure-pytest plugin generates report even when AUTO_GENERATE_ALLURE=false
- **Attempted Fixes**:
  - Commented out addopts in pytest.ini
  - Added `config.option.allure_report_dir = None` in conftest.py
- **Final Solution**: None fully worked - allure still runs but test completes now

#### 3. Pre-existing Test Data Issue
- **Test**: login-11-INVALID_DATA
- **Problem**: Test data has `"country": "Florida"` but website dropdown expects actual country names
- **Status**: Pre-existing issue, not related to our changes

### Commands to Remember

```bash
# Run specific test with full traceback
pytest -n 0 "path/to/test.py::test_name" --tb=long

# Find test failures in allure results (faster than rerunning)
grep -r "status.*broken" allure-results/

# Run tests by marker
pytest -n auto -m "TC3 or TC2"

# Quick collection without allure blocking
python -m pytest --collect-only -q
```

### Rules for Agentic AI Testing

1. **Always check allure-results for actual error** - Don't rely on console output alone
2. **Verify method names match between step definitions and page objects** - Use grep to find inconsistencies
3. **Check test data validity** - Invalid data in JSON can cause timeout failures
4. **Page objects should expose properties** - Use `@property` decorators for API clients (e.g., `all_products`)
5. **Step definitions should be thin** - Keep logic in page objects for maintainability

### Project Structure Reference

```
src/pages/
├── api/
│   ├── base_api.py          # ApiBasePage class with all_products property
│   ├── get/
│   │   ├── get_all_product_list.py
│   │   └── get_all_brands_list.py
│   └── post/
│       └── post_to_all_products_list.py
└── ui/
    └── (UI page objects)

tests/step_definitions/
├── api/
│   └── products/get/test_api_products_list.py  # Fixed method references
└── ui/
    └── (UI step definitions)
```