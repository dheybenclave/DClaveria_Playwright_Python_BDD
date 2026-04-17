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

---

## Session: 2026-04-14

### Commands & Prompts Executed

| # | Command/Prompt | Purpose | Result |
|---|----------------|---------|--------|
| 1 | `pytest -m api` | Run API tests | 10 passed, 11 failed |
| 2 | Read API docs `automationexercise.com/api_list` | Verify endpoints | Found correct endpoints |
| 3 | Fixed feature file endpoints | Change loginUser→verifyLogin, 200→201 | Fixed TC101 |
| 4 | Fixed TestDataManager field mapping | Include all fields even empty | Fixed birth_day mapping |
| 5 | Fixed API page objects | Changed data= → form= | Fixed create/update/delete |

### Key Learnings

#### 1. Playwright `data=` vs `form=` - CRITICAL
- **Problem**: API tests returning 400 errors
- **Root Cause**: Playwright's `APIRequestContext.post(data=...)` sends JSON-encoded body, but the API expects form-encoded data (`application/x-www-form-urlencoded`)
- **Fix**: Use `form=data` instead of `data=data` in API requests
- **Files Fixed**:
  - `src/pages/api/user/create_account.py`
  - `src/pages/api/user/update_account.py`
  - `src/pages/api/user/delete_account.py`
  - `src/pages/api/order/create_order.py`

#### 2. API Documentation Verification
- **Reference**: https://automationexercise.com/api_list
- **Verified Endpoints**:
  - `/api/createAccount` → returns responseCode 201 (not 200)
  - `/api/verifyLogin` → correct endpoint (not `/api/loginUser`)
  - `/api/deleteAccount` → requires DELETE method (not POST)
- **Required Fields**: Many fields required (firstname, address1, etc.)

#### 3. TestDataManager Field Mapping Bug
- **Problem**: API rejecting requests with 400 errors
- **Root Cause**: Field mapping filtered out empty values, but API requires all fields
- **Fix**: Include all fields even if empty string

### Commands to Remember

```bash
# Run API tests only
pytest -m api -v

# Verify endpoint with curl (for debugging)
curl -X POST https://automationexercise.com/api/createAccount \
  -d "name=test&email=test@example.com&password=test123"

# Debug API request - check form vs data encoding
# Use form= for form-encoded, data= for JSON
request_context.post(url, form=data)  # For form-encoded
request_context.post(url, data=json)   # For JSON
```

### Files Modified This Session

```
AGENTS.md                                    # Updated (220 lines)
tests/features/api_suites/
│   └── validate_verify_user_api.feature       # Fixed endpoints
utils/
│   └── api_helpers.py                     # Fixed field mapping
src/pages/api/user/
│   ├── create_account.py                  # Changed data=→form=
│   ├── update_account.py                  # Changed data=→form=
│   └── delete_account.py                  # Changed data=→form=
src/pages/api/order/
│   └── create_order.py                    # Changed data=→form=
```

### Remaining Issues

- ~~User API tests (TC101, TC103-TC105, TC109, TC110)~~ - FIXED
- ~~Order API tests (TC201-TC205)~~ - SKIPPED (endpoints don't exist in API docs)

---

## Session: 2026-04-14 (Continued)

### New Issues Fixed

#### 4. Test Data - Duplicate Email Problem
- **Problem**: Test users all had same email causing "Email already exists" errors
- **Fix**: Added unique email suffix using UUID to each test user
- **File**: `tests/test_datas/json/register_user_data.json`

#### 5. Missing Step Definition for "success message"
- **Problem**: TC103 failed with "Step definition not found" for "the response should contain a success message"
- **Fix**: Added `verify_login_success_message` step definition in `tests/step_definitions/api/user/test_user_api.py`

#### 6. DELETE Method Routing
- **Problem**: Feature file used DELETE method but step definition was catching POST
- **Fix**: Added explicit DELETE handler `delete_account_with_delete_method` and modified generic handler to route DELETE to it

#### 7. Order API Endpoints Don't Exist
- **Problem**: TC201-TC205 use endpoints `/api/createOrder`, `/api/getOrderByOrderId`, `/api/getOrders` which don't exist
- **Fix**: Added `@skip` tag to feature file to disable these tests

### Final Results

```
================ 16 passed, 5 skipped, 28 deselected ================
```

### Files Modified (Continued)

```
tests/test_datas/json/register_user_data.json     # Unique emails
tests/step_definitions/api/user/test_user_api.py  # Added steps, fixed routing
tests/features/api_suites/
  ├── validate_verify_order_api.feature           # @skip order tests
  └── validate_verify_user_api.feature            # Already fixed
```