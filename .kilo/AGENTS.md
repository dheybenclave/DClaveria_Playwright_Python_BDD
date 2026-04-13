# AGENTS.md - Unified AI Agent Coding Guidelines

This document provides commands and code style guidelines for **all AI coding agents** operating in this Playwright Python BDD test automation project. It applies to Claude, Cursor, and Kilo.

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

## Design Principles

- **Thin steps, rich pages**: Step definitions delegate to page objects; page objects own locators, actions, and assertions
- **Data-driven BDD**: Tables in feature files flow directly into verifications
- **Marker-driven execution**: Use `@TC#`, `@ui`, `@api`, `@regression` tags for test selection
- **Centralized timeouts**: Default 15-second timeout in `conftest.py`

---

## Build/Lint/Test Commands

```bash
# === Test Execution ===
pytest                           # Run all tests
pytest --collect-only           # Verify test discovery (always run before committing)
pytest -m "TC6"                # Run single test by marker
pytest -m "TC6 or TC7"         # Run multiple markers
pytest -m api                  # Run API tests
pytest -k "login"               # Run tests matching keyword
pytest -n auto                  # Run tests in parallel
HEADLESS=false pytest -m TC6   # Run with visible browser

# === Linting & Formatting ===
python -m flake8 src/ tests/    # Run flake8 linter
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

# With video recording for debugging
HEADLESS=false pytest -m TC6 -v
```

### Pytest Configuration

```ini
[pytest]
pythonpath = .
testpaths = tests
bdd_features_base_dir = features/
addopts = --html=test-results/reports/report.html --self-contained-html -s -vv
markers =
    ui: UI E2E tests
    api: API CRUD tests
    regression: full suite
    TC: dynamic test case marker (e.g., @pytest.mark.TC1)
    login: Login Page Test
```

---

## Environment Variables

- `BASE_URL` — Target site (default: https://automationexercise.com)
- `HEADLESS` — Browser mode (default: true)
- `RECORD_VIDEO` — Capture video on test (default: false)
- `AUTO_GENERATE_ALLURE` — Auto-generate Allure reports (default: false)
- `ADMIN_EMAIL`, `ADMIN_PASSWORD` — Admin credentials

---

## Code Style Guidelines

### Imports

- Use absolute imports: `from src.pages.login_page import LoginPage`
- Group imports in order: standard library, third-party, local

```python
# Standard library
import csv
import logging
from typing import Optional

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
- Use `Optional[X]` for nullable parameters, `List[Type]`, `Dict[Key, Value]` from typing

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Classes | PascalCase | `LoginPage`, `UIBasePage` |
| Methods | snake_case | `login_credentials_by_role` |
| Variables | snake_case | `username`, `btn_login` |
| Constants | UPPER_SNAKE_CASE | `MAX_TIMEOUT`, `DEFAULT_URL` |
| Locators | `txt_`, `btn_`, `lbl_` prefix | `txt_username`, `btn_login` |

### Error Handling

- Use specific exception types with context in error messages
- Log errors before raising

```python
try:
    creds = Config.get_credentials(role)
except (EnvironmentError, ValueError, KeyError) as e:
    self.logger.warning(f"Config lookup failed: {e}")
    raise ValueError(f"Role '{role}' not found") from e
```

---

## Page Object Pattern

- All locators defined as `@property` methods returning `Locator`
- Keep step definitions declarative and minimal
- Delegate UI actions to page objects

```python
class LoginPage(UIBasePage):
    @property
    def txt_username(self) -> Locator:
        return self.page.locator("[data-qa='login-email']")

    @property
    def btn_login(self) -> Locator:
        return self.page.locator("button[data-qa='login-button']")

    def login_credentials(self, username: str, password: str) -> None:
        self.common_page.enter_text(self.txt_username, username)
        self.common_page.enter_text(self.txt_password, password)
        self.btn_login.click()
```

---

## Step Definitions

- Keep steps thin - delegate to page objects
- Use `parsers.parse()` for parameterized steps
- Include clear assertion messages
- Do not introduce duplicate BDD step patterns for the same sentence

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
- Avoid brittle CSS selectors - prefer `[data-qa]` attributes
- Prefer deterministic waits/assertions over sleeps

---

## Security Requirements

- Never hardcode credentials, tokens, or API keys
- Load secrets from `.env` or environment variables
- Never print full secret values in logs
- Validate external input before URL construction

```python
# GOOD: Mask credentials in logs
masked_user = f"{username[:3]}***@{domain}"
logger.info(f"Logged in as {masked_user}")
```

---

## API Testing Pattern

- **Reference style**:
  - `tests/features/api_suites/validate_verify_all_product_list_api.feature`
  - `tests/features/api_suites/validate_verify_all_brands_list_api.feature`
  - `tests/step_definitions/api/test_api_get_all_product_list.py`
- **Base API accessor**: `src/pages/api/base_api.py`
- Access via `pages.api.*` in step definitions

---

## Reporting Rules

- `pytest-html` output goes to `test-results/reports/`
- Allure raw results go to `allure-results/`
- Allure HTML is auto-generated at session end to `allure-report/` (when `allure` or `npx allure` is available)
- Manual open:
  - `npx allure open allure-report`
  - `npx allure serve allure-results`

---

## Unified AI Platform Configuration

This project uses **three AI platforms** that must stay synchronized.

### Platform Configurations

| Platform | Config File | Rules Directory | Hooks |
|----------|-------------|-----------------|-------|
| Claude | `.claude/settings.json` | `.claude/rules/` | `.claude/hooks/` |
| Cursor | `.cursor/hooks.json` | `.cursor/rules/` | `.cursor/hooks/` |
| Kilo | `.kilo/kilo.json` | `.kilo/rules/` | `.kilo/hooks/` |

### Cross-Platform Reference

All AI platforms reference the **same core rules**:
- `common-testing.md` - Testing requirements and stability rules
- `python-coding-style.md` - Python code style
- `python-security.md` - Security best practices
- `playwright-python-framework.md` - Framework workflow
- `test-automation-guardrails.md` - Core guardrails

### Agentic Commands

Available as slash commands in respective platforms:
- `/feature-development` — Add new feature files and corresponding steps
- `/test-debugging` — Triage failing tests
- `/self-heal-tests` — Fix flaky selectors with locator fallbacks
- `/generate-test-cases` — Generate tests from requirements
- `/plan-regression-suite` — Plan marker-based regression suites

### Session Start Actions

Each platform runs its own session start hook to verify environment:
- **Claude**: `.claude/hooks/session_start.py`
- **Cursor**: `.cursor/hooks/session_start.py`
- **Kilo**: `.kilo/hooks/session_start.py`

### Pre-Prompt Security Checks

Each platform validates prompts for secrets before submission:
- **Claude**: `.claude/hooks/user_prompt_submit.py`
- **Cursor**: `.cursor/hooks/before_submit_prompt.py`
- **Kilo**: `.kilo/hooks/before_prompt_submit.py`

---

## MCP Servers

| Platform | MCP Server | Config Location |
|----------|------------|-----------------|
| Claude | playwright-local, filesystem-project | `.claude/settings.json` |
| Cursor | @playwright/mcp | `.cursor/mcp.json` |
| Kilo | @playwright/mcp | `.kilo/kilo.json` |

---

## Sync Strategy

When updating any rule or configuration:

1. **Make the change** in the primary location
2. **Copy to all three directories**:
   - `.claude/rules/` → Claude Desktop
   - `.cursor/rules/` → Cursor
   - `.kilo/rules/` → Kilo
3. **Update hooks** if behavior changes
4. **Run validation**: `pytest --collect-only`

---

## Quick Reference by Platform

### Claude (/.claude)
- **Commands**: `.claude/commands/` - test-debugging, self-heal-tests, feature-development, plan-regression-suite, generate-test-cases, agentic-ci-cd, agentic-bootstrap
- **Agents**: `.claude/agents/` - qa-test-automation-engineer, test-architect, product-owner-business-analyst, scrum-team-leader

### Cursor (/.cursor)
- **Rules**: `.cursor/rules/` - python-coding-style.md, python-testing.md, playwright-python-framework.md, python-security.md, common-testing.md
- **Skills**: `.cursor/skills/init/` - Environment initialization
- **MCP**: `.cursor/mcp.json`

### Kilo (/.kilo)
- **Commands**: `.kilo/command/` - verify, collect, debug, test
- **Agents**: `.kilo/agent/` - test-planner, test-healer, test-generator
- **MCP**: `.kilo/mcp/fastmcp_server.py` - AI-powered test execution

---

## Platform-Specific Documentation

For detailed configuration of each AI platform, see:

- **[CLAUDE.md](./CLAUDE.md)** - Claude-specific configuration (settings, hooks, commands, agents)
- **[CURSOR.md](./CURSOR.md)** - Cursor-specific configuration (MCP, hooks, rules, skills)
- **[KILO.md](./KILO.md)** - Kilo-specific configuration (commands, agents, FastMCP server, hooks)

---

## Done Criteria for Test Changes

- Scenario updates are reflected in matching step/page layers
- `pytest --collect-only -q` passes
- Relevant marker run passes (`api`, `TC#`, or targeted suite)
- Report artifacts generated in `test-results/`

---

## Related Documentation

- [Claude AGENTIC_QA_GUIDE](./.claude/AGENTIC_QA_GUIDE.md)
- [Cursor AGENTIC_QA_GUIDE](./.cursor/AGENTIC_QA_GUIDE.md)
- [Kilo AGENTIC_QA_GUIDE](./.kilo/AGENTIC_QA_GUIDE.md)