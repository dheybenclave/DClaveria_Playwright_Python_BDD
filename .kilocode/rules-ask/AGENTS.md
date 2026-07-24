# AGENTS.md - Ask Mode Rules

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Documentation Context

### Project Structure
- **Features**: `tests/features/` - Gherkin `.feature` files organized by suite type
- **Steps**: `tests/step_definitions/` - Auto-discovered via glob pattern in `conftest.py`
- **Pages**: `src/pages/` - Page objects for UI and API
- **Data**: `tests/test_datas/` - JSON/CSV test data files

### Key Non-Obvious Patterns
- **Auto-discovery**: Step definitions are auto-imported by `conftest.py` - no manual imports needed
- **Unified pages fixture**: `pages` fixture provides `pages.ui` and `pages.api` access
- **Test data loading**: Use `Config.get_test_data()` instead of direct file reads

### Reporting Artifacts
- **HTML report**: `test-results/reports/report.html` (self-contained)
- **Allure**: `allure-results/` (raw) → `allure-report/` (generated)
- **Screenshots**: `test-results/screenshots/` (on failure only)
- **Videos**: `test-results/videos/` (when `RECORD_VIDEO=true`, on failure only)

### Environment Setup
- **Copy `.env.example` to `.env`** for local development
- **Required**: `BASE_URL` (https://automationexercise.com)
- **Optional**: `HEADLESS`, `RECORD_VIDEO`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`