# AGENTS.md - Architect Mode Rules

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Architectural Constraints

### Test Discovery Architecture
- **Auto-import mechanism**: `conftest.py` uses `glob.glob("tests/step_definitions/**/*.py")` to auto-discover step definitions
- **No manual imports**: Step files are dynamically imported via `config.pluginmanager.import_plugin()`
- **File naming**: Files named `test_*.py` or `*_test.py` are auto-discovered; others use the glob pattern

### Page Object Architecture
- **Locator pattern**: All locators are `@property` methods returning `Locator` objects
- **Naming convention**: `txt_`, `btn_`, `lbl_` prefixes for textboxes, buttons, labels
- **Base classes**: `UIBasePage` (UI) and `ApiBasePage` (API) in `src/pages/`

### Test Data Architecture
- **Central config**: `utils/config.py` provides `Config.get_test_data()` for loading JSON/CSV
- **Data location**: `tests/test_datas/` directory
- **Never hardcode**: Test data must be loaded from files, not inline in code

### Reporting Architecture
- **HTML reports**: `test-results/reports/report.html` (self-contained)
- **Allure**: `allure-results/` → `allure-report/` (auto-served when `AUTO_GENERATE_ALLURE=true`)
- **Artifacts**: Screenshots on failure, videos when `RECORD_VIDEO=true`

### Environment Architecture
- **Required**: `BASE_URL` (https://automationexercise.com)
- **Optional**: `HEADLESS`, `RECORD_VIDEO`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`
- **Copy `.env.example` to `.env`** for local development