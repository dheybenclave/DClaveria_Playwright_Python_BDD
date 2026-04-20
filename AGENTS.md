# AGENTS.md - Unified AI Agent Coding Guidelines

**Applies to:** Claude, Cursor, Kilo, and all GitHub Agents  
**Domain:** UI + API automation for `https://automationexercise.com`  
**Stack:** Playwright (Python sync) · Pytest · pytest-bdd · pytest-html · allure-pytest

---

## 1. Project Structure

```
DClaveria_Playwright_Python_BDD/
├── tests/
│   ├── features/                    # Gherkin .feature files
│   │   ├── e2e_suites/              # Full user journey flows
│   │   ├── regression_suites/       # Critical path validation
│   │   ├── api_suites/              # REST API CRUD operations
│   │   ├── security_suites/         # XSS, SQLi, auth tests
│   │   └── accessibility_suites/    # WCAG validations
│   ├── step_definitions/            # Thin step glue
│   │   ├── ui/                      # login, sign_up, products, checkout, payment, common
│   │   ├── api/                     # user, order, search, brands, products
│   │   ├── security/                # authentication, xss, sql_injection
│   │   └── accessibility/           # a11y checks
│   └── test_datas/                  # JSON, CSV data files
├── src/pages/
│   ├── ui/                          # Rich UI page objects
│   ├── api/                         # API client layer
│   ├── base_page.py                 # Core UI base class
│   └── common_page.py               # Shared UI utilities
├── utils/
│   ├── config.py                    # Environment & secrets loader
│   ├── logger.py                    # Structured logging
│   ├── test_state.py                # Cross-step state sharing
│   ├── api_helpers.py               # HTTP session helpers
│   └── security_payloads.py         # Security test vectors
├── conftest.py                      # Pytest fixtures & hooks
├── pytest.ini                       # Pytest config (markers, timeout)
├── requirements.txt                 # Python dependencies
├── test-results/                    # HTML reports, screenshots, videos
├── allure-results/                  # Allure raw JSON results
├── .env                             # Local secrets (git-ignored)
├── .github/workflows/               # CI/CD pipelines
├── scripts/                         # Bootstrap & helper scripts
│
├── .claude/                         # Claude AI config & agents
│   ├── settings.json
│   ├── commands/
│   ├── agents/
│   ├── hooks/
│   └── rules/
├── .cursor/                         # Cursor AI config & agents
│   ├── hooks.json
│   ├── mcp.json
│   ├── commands/ (shared)
│   ├── agents/ (shared)
│   ├── skills/
│   └── rules/
└── .kilo/                           # Kilo AI config & agents
    ├── kilo.json
    ├── command/
    ├── agent/
    ├── mcp/
    ├── hooks/
    └── rules/
```

---

## 2. Build/Lint/Test Commands

### Test Execution

```bash
# Run all tests
pytest

# Verify test discovery (always run before committing)
pytest --collect-only

# Run single test by marker (preferred)
pytest -m "TC6"

# Run multiple markers
pytest -m "TC6 or TC7"

# Run by test type
pytest -m api                    # API tests only
pytest -m ui                     # UI tests only
pytest -m regression             # Regression suite

# Run by keyword in scenario name
pytest -k "login"

# Parallel execution
pytest -n auto

# Headed mode (visible browser for debugging)
HEADLESS=false pytest -m TC6 -v

# Generate HTML report
pytest --html=test-results/reports/report.html --self-contained-html

# With video recording
RECORD_VIDEO=true pytest -m TC6

# Allure reporting
pytest --alluredir=allure-results
```

### Linting & Formatting

```bash
# Linting
python -m flake8 src/ tests/

# Type checking
python -m mypy src/

# Formatting checks
python -m black --check .
python -m isort --check .
```

---

## 3. Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `BASE_URL` | https://automationexercise.com | Yes | Target application URL |
| `HEADLESS` | true | No | Run browser in headless mode |
| `RECORD_VIDEO` | false | No | Record test videos on failure |
| `PLAYWRIGHT_DEFAULT_TIMEOUT` | 15000 | No | Global timeout in milliseconds |
| `ADMIN_EMAIL` | - | No | Admin account email |
| `ADMIN_PASSWORD` | - | No | Admin account password |
| `LIST_OF_CREDENTIALS` | - | No | JSON array of test credentials |
| `AUTO_GENERATE_ALLURE` | false | No | Auto-generate Allure HTML reports |

---

## 4. Code Style Guidelines

### Imports

Use absolute imports, grouped in order: standard library, third-party, local.

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

## 5. Page Object Pattern

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

## 6. Step Definitions

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

## 7. Reliability Rules

- Use explicit waits: `page.wait_for_load_state()`, `expect(locator).to_be_visible(timeout=10000)`
- Never use `time.sleep()` - use deterministic waits
- Keep selectors in page objects, not steps
- Prefer `[data-qa]` attribute selectors over brittle CSS

---

## 8. Security Requirements

- Never hardcode credentials, tokens, or API keys
- Load secrets from `.env` or environment variables
- Mask credentials in logs: `f"{username[:3]}***@{domain}"`
- Validate external input before using it in assertions or URL construction

---

## 9. Design Principles

- **Thin steps, rich pages**: Step definitions delegate to page objects
- **Data-driven BDD**: Tables in feature files flow into verifications
- **Marker-driven execution**: Use `@TC#`, `@ui`, `@api`, `@regression` tags
- **Centralized timeouts**: Default 15-second timeout in `conftest.py`

---

## 10. Defined of Done (Testing)

- [ ] Scenario(s) pass
- [ ] `pytest --collect-only` passes
- [ ] No flaky waits or timing hacks
- [ ] Report artifacts in `test-results/`

---

## 11. Rules Integration

This project includes Kilo-specific rules in `.kilo/rules/`:

- `python-coding-style.md` - Python coding style (PEP 8, type hints, readability)
- `python-testing.md` - pytest and pytest-bdd guidance
- `python-security.md` - Security best practices
- `common-testing.md` - Testing requirements and stability rules
- `playwright-python-framework.md` - Framework workflow conventions
- `test-automation-guardrails.md` - Test Automation Guardrails

**All platforms (Claude, Cursor, Kilo) reference the same core rule set** — keep them synchronized when making changes. See `.kilo/AGENTS.md` for platform-specific details.

---

## 12. AI Agent Configuration

### Platform Overview

| Platform | Config File | Rules Directory | Hooks | Docs |
|----------|-------------|-----------------|-------|------|
| Claude | `.claude/settings.json` | `.claude/rules/` | `.claude/hooks/` | CLAUDE.md |
| Cursor | `.cursor/hooks.json` | `.cursor/rules/` | `.cursor/hooks/` | CURSOR.md |
| Kilo | `.kilo/kilo.json` | `.kilo/rules/` | `.kilo/hooks/` | KILO.md |

### Session Start Actions

Each platform runs startup hooks to verify environment:

```bash
# Verify environment (all platforms)
python .cursor/skills/init/scripts/verify_env.py

# Collect tests
python .cursor/skills/init/scripts/smoke_collect.py
```

### Sync Strategy

When updating rules:

1. Make change in primary location (`.kilo/rules/`)
2. Copy to all three directories: `.claude/rules/`, `.cursor/rules/`
3. Run `pytest --collect-only` to validate

---

## 13. Pytest Markers Reference

| Marker | Description |
|--------|-------------|
| `@TC#` | Specific test case ID (e.g., `@TC6`, `@TC7`) |
| `@ui` | UI/E2E tests |
| `@api` | API CRUD tests |
| `@regression` | Full regression suite |
| `@login` | Login page tests |
| `@signup` | Sign-up page tests |
| `@products` | Products page tests |
| `@checkout` | Checkout flow tests |
| `@payment` | Payment tests |
| `@positive_testing` | Happy path scenarios |
| `@negative_testing` | Error/edge case scenarios |
| `@security` | Security-focused tests (XSS, SQLi, auth) |

---

## 14. Reporting Artifacts

| Artifact | Location | Description |
|----------|----------|-------------|
| HTML Report | `test-results/reports/report.html` | Self-contained HTML report |
| Allure Results | `allure-results/` | Raw Allure JSON |
| Allure HTML | `allure-report/` | Generated Allure HTML |
| Screenshots | `test-results/screenshots/` | Screenshots on failure |
| Videos | `test-results/videos/` | Test videos when RECORD_VIDEO=true |
| Logs | `test-results/pytest-logs.log` | DEBUG level logs |

---

## 15. MCP Servers

| Platform | MCP Server | Config Location |
|----------|------------|-----------------|
| Claude | playwright-local, filesystem-project | `.claude/settings.json` |
| Cursor | @playwright/mcp | `.cursor/mcp.json` |
| Kilo | @playwright/mcp | `.kilo/kilo.json` |

---

## 16. Quick Start Summary

```bash
# 1. Setup
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install --with-deps

# 2. Verify
pytest --collect-only

# 3. Run tests
pytest -m TC6

# 4. Debug
HEADLESS=false pytest -m TC6 -v
```

---

**For platform-specific commands and agents, see:**  
- [CLAUDE.md](./CLAUDE.md)  
- [CURSOR.md](./CURSOR.md)  
- [KILO.md](./KILO.md)  
- [AGENTIC_GUIDE.md](./AGENTIC_GUIDE.md)
