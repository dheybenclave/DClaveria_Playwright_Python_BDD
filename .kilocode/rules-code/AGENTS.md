# AGENTS.md - Code Mode Rules

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Coding Rules

### Page Object Pattern
- **All locators as `@property` methods returning `Locator`** - never inline selectors in steps
- **Locator naming**: Use `txt_`, `btn_`, `lbl_` prefixes (e.g., `txt_username`, `btn_login`)
- **Thin steps, rich pages**: Steps delegate to page objects; max 3 lines per step definition

### Test Data Management
- **Load test data via `Config.get_test_data()`** from `tests/test_datas/` directory
- **Never hardcode test data** in page objects or step definitions

### Security
- **Mask credentials in logs**: `f"{username[:3]}***@{domain}"`
- **Never print full secret values** in test output