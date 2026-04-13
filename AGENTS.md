# AGENTS.md - AI Agent Coding Guidelines

This document provides commands and code style guidelines for AI coding agents operating in this Playwright Python BDD test automation project.

---

## Project Overview

- **Stack**: Playwright (Python sync), `pytest`, `pytest-bdd`, `pytest-html`, `allure-pytest`
- **Domain**: UI + API automation for `https://automationexercise.com`
- **Framework**: pytest-bdd with thin step definitions and rich page objects

## Architecture

| Path | Description |
|------|-------------|
| `tests/features/*.feature` | Gherkin scenarios with `@TC#` markers |
| `tests/step_definitions/ui/` | Declarative step glue (thin) |
| `tests/step_definitions/api/` | API step definitions |
| `src/pages/` | Page objects with locators and assertions (rich) |
| `src/pages/api/` | API page-object layer |
| `utils/` | Environment handling, logging utilities |
| `test-results/` | HTML reports, screenshots/videos on failure |

---

## Build/Lint/Test Commands

```bash
# Test Execution
pytest                           # Run all tests
pytest --collect-only            # Verify test discovery (always run before committing)
pytest -m "TC6"                  # Run single test by marker
pytest -m "TC6 or TC7"          # Run multiple markers
pytest -m api                    # Run API tests
pytest -k "login"                # Run tests matching keyword
pytest -n auto                   # Run tests in parallel
HEADLESS=false pytest -m TC6    # Run with visible browser

# Linting & Formatting
python -m flake8 src/ tests/     # Run flake8 linter
python -m mypy src/             # Type checking with mypy
python -m black --check .       # Check formatting
python -m isort --check .       # Check import order
```

### Running a Single Test

```bash
# By marker (preferred)
pytest -m TC6

# By keyword in scenario name
pytest -k "login success"

# By feature file
pytest tests/features/regression_suites/validate_verify_login.feature
```

### Environment Variables

- `BASE_URL` — Target site (default: https://automationexercise.com)
- `HEADLESS` — Browser mode (default: true)
- `RECORD_VIDEO` — Capture video on test (default: false)

---

## Code Style Guidelines

### Imports

Use absolute imports, group in order: standard library, third-party, local.

```python
# Standard library
import csv
import logging
from typing import Optional, List, Dict

# Third-party
from playwright.sync_api import Locator, Page, expect
from pytest_bdd import when, parsers, given, then

# Local application
from src.pages.base_page import UIBasePage
from utils.config import Config
```

### Formatting & Types

- Maximum line length: 120 characters
- Use 4 spaces for indentation (no tabs)
- Add type hints for all function parameters and return types
- Use `Optional[X]` for nullable, `List[Type]`, `Dict[Key, Value]`

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `LoginPage`, `UIBasePage` |
| Methods | snake_case | `login_credentials_by_role` |
| Variables | snake_case | `username`, `btn_login` |
| Constants | UPPER_SNAKE_CASE | `MAX_TIMEOUT`, `DEFAULT_URL` |
| Locators | `txt_`, `btn_`, `lbl_` prefix | `txt_username`, `btn_login` |

### Error Handling

Use specific exception types with context. Log errors before raising.

```python
try:
    creds = Config.get_credentials(role)
except (EnvironmentError, ValueError, KeyError) as e:
    self.logger.warning(f"Config lookup failed: {e}")
    raise ValueError(f"Role '{role}' not found") from e
```

---

## Page Object Pattern

All locators as `@property` methods returning `Locator`. Keep step definitions minimal.

```python
class LoginPage(UIBasePage):
    @property
    def txt_username(self) -> Locator:
        return self.page.locator("[data-qa='login-email']")

    @property
    def btn_login(self) -> Locator:
        return self.page.locator("button[data-qa='login-button']")

    def login(self, username: str, password: str) -> None:
        self.common_page.enter_text(self.txt_username, username)
        self.common_page.enter_text(self.txt_password, password)
        self.btn_login.click()
```

---

## Step Definitions

Keep steps thin - delegate to page objects. Use `parsers.parse()` for parameterized steps.

```python
from pytest_bdd import when, parsers, then

@when(parsers.parse("I enter credentials using the {user_role} role"))
def enter_credentials_using_role(pages, user_role):
    pages.ui.login_page.login_credentials_by_role(role=user_role)

@then("I should see the dashboard")
def verify_dashboard(pages):
    expect(pages.ui.login_page.btn_logout).to_be_visible()
```

---

## Reliability Rules

- Use explicit waits: `page.wait_for_load_state()`, `expect(locator).to_be_visible(timeout=10000)`
- Never use `time.sleep()` - use deterministic waits
- Keep selectors in page objects, not steps
- Prefer `[data-qa]` attribute selectors over brittle CSS

---

## Security Requirements

- Never hardcode credentials, tokens, or API keys
- Load secrets from `.env` or environment variables
- Mask credentials in logs: `f"{username[:3]}***@{domain}"`

---

## Done Criteria for Test Changes

- [ ] Scenario(s) pass
- [ ] `pytest --collect-only` passes
- [ ] No flaky waits or timing hacks
- [ ] Report artifacts in `test-results/`

---

## Design Principles

- **Thin steps, rich pages**: Step definitions delegate to page objects
- **Data-driven BDD**: Tables in feature files flow into verifications
- **Marker-driven execution**: Use `@TC#`, `@ui`, `@api`, `@regression` tags
- **Centralized timeouts**: Default 15-second timeout in `conftest.py`