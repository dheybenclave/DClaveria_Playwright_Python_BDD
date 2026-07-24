# Agentic QA Guide — Unified Workflow

This guide unifies Kilo and Claude AI agent workflows for the Playwright Python BDD framework.

## Overview

Both AI platforms share:
- **Same rule set** (`.kilo/rules/` and `.claude/rules/` are synchronized copies)
- **Same test structure** (`tests/features/`, `src/pages/`, `utils/`)
- **Same execution model** (pytest + pytest-bdd, marker-driven)

---

## Quick Start

```powershell
# 1. Setup
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install --with-deps

# 2. Verify environment (all platforms)
pytest --collect-only

# 3. Run targeted tests
pytest -m "TC6"
```

---

## Platform Cheatsheet

| Platform | Init/Verify | Config | Agents | Commands | Skills |
|----------|------------|--------|--------|----------|--------|
| **Kilo** | `.kilo/hooks/session_start.py` | `.kilo/kilo.json` | `.kilo/agent/` | `.kilo/command/` | `.kilo/skills/` |
| **Claude** | `.claude/hooks/session_start.py` | `.claude/settings.json` | `.claude/agents/` | `.claude/commands/` | — |

---

## Unified Rules (All Platforms)

The 5 core rule files are synchronized across all platforms:

1. **common-testing.md** — Validation sequence, DoD, stability rules
2. **python-coding-style.md** — PEP 8, type hints, naming conventions
3. **python-security.md** — Secrets management, logging safety
4. **playwright-python-framework.md** — Workflow, paths, commands
5. **test-automation-guardrails.md** — Selectors, waits, BDD discipline

**Synchronized copies**: Rules are maintained in both `.kilo/rules/` and `.claude/rules/`.

---

## Test Execution Matrix

| Need | Command |
|------|---------|
| Run all tests | `pytest` |
| Run specific test case | `pytest -m TC6` |
| Run by tag (ui/api/regression) | `pytest -m ui` / `pytest -m api` |
| Run by keyword | `pytest -k "login"` |
| Parallel execution | `pytest -n auto` |
| Visible browser (debug) | `HEADLESS=false pytest -m TC6 -v` |
| With video | `RECORD_VIDEO=true pytest -m TC6` |
| HTML report | `pytest --html=test-results/reports/report.html` |
| Allure | `pytest --alluredir=allure-results` |
| Verify discovery | `pytest --collect-only` |

---

## Core Guardrails (Non-Negotiable)

1. **NO selectors in step definitions** — All selectors in page objects (`src/pages/`)
2. **NO time.sleep()** — Use `expect(locator).to_be_visible()`, `page.wait_for_load_state()`
3. **NO long step definitions** — Keep steps focused and minimal; delegate complex logic to page objects
4. **NO hardcoded secrets** — Use `.env`, `Config` class
5. **ALWAYS run `--collect-only` before commit**
6. **ALWAYS tag scenarios with `@TC#` markers**
7. **ALWAYS use semantic selectors** — `get_by_role()`, `get_by_label()`, `[data-qa]`
8. **ALWAYS verify with targeted run then collection**

---

## Framework Rules Reference

### Selector Strategy (Priority Order)

```python
# 1. Semantic (best)
page.get_by_role("button", name="Add to cart")
page.get_by_label("Email")
page.get_by_placeholder("Search...")

# 2. Data attributes (good)
page.locator("[data-qa='login-btn']")
page.locator("[data-testid='submit']")

# 3. CSS (avoid if possible)
page.locator(".btn.btn-primary")  # fragile
page.locator("#submit")  # may change
```

### Wait Strategy

```python
# ❌ NEVER
time.sleep(2)

# ✅ ALWAYS
page.wait_for_load_state("networkidle")
expect(locator).to_be_visible(timeout=10000)
locator.wait_for(state="attached")
```

### Page Object Pattern

```python
class LoginPage(UIBasePage):
    @property
    def txt_email(self) -> Locator:
        return self.page.locator("[data-qa='login-email']")

    def login(self, email: str, password: str) -> None:
        self.common_page.enter_text(self.txt_email, email)
        self.common_page.enter_text(self.txt_password, password)
        self.btn_login.click()
```

### Step Definition Pattern

```python
@when(parsers.parse("I login with role {role}"))
def step_impl(pages, role):
    pages.ui.login_page.login_credentials_by_role(role)

@then("I should see the dashboard")
def step_impl(pages):
    expect(pages.ui.home_page.btn_logout).to_be_visible()
```

---

## Debugging Workflow

1. **Check collection**: `pytest --collect-only`
2. **Run single test**: `pytest -m TC6 -v`
3. **Visible browser**: `HEADLESS=false pytest -m TC6 -v --stepwise`
4. **Check artifacts**: `test-results/screenshots/`, `test-results/videos/`
5. **Use healer**: `kilo "Use test-healer to fix selector failures"`
6. **Inspect page**: Use Playwright Inspector (`page.pause()`)

---

## Reporting

| Artifact | Location |
|----------|----------|
| HTML report | `test-results/reports/report.html` |
| Screenshots | `test-results/screenshots/` (on failure) |
| Videos | `test-results/videos/` (if `RECORD_VIDEO=true`) |
| Allure raw | `allure-results/` |
| Allure HTML | `allure-report/` (auto-generated) |

Open Allure:
```bash
npx allure open allure-report
npx allure serve allure-results
```

---

## Platform-Specific Notes

### Kilo
- Uses FastMCP server (`.kilo/mcp/fastmcp_server.py`) for AI tool integration
- Commands accessible via `kilo "<command>"` syntax
- Hooks run automatically on session start/file edit

### Claude
- MCP via `playwright-local` in `.claude/settings.json`
- Commands via `.claude/commands/` (e.g., `feature-development`, `test-debugging`, `generate-test-cases`, `plan-regression-suite`, `self-heal-tests`, `agentic-ci-cd`, `agentic-bootstrap`)
- Agents in `.claude/agents/` (qa-test-automation-engineer, test-architect, test-generator, test-healer, test-planner, product-owner-business-analyst, scrum-team-leader)

---

## Environment Variables

| Variable | Default | Required | Purpose |
|----------|---------|----------|---------|
| `BASE_URL` | https://automationexercise.com | Yes | Target site |
| `HEADLESS` | true | No | Headless mode |
| `RECORD_VIDEO` | false | No | Capture test videos |
| `PLAYWRIGHT_DEFAULT_TIMEOUT` | 15000 | No | Global timeout (ms) |
| `ADMIN_EMAIL` | — | No | Admin account |
| `ADMIN_PASSWORD` | — | No | Admin password |
| `LIST_OF_CREDENTIALS` | — | No | JSON test credentials |
| `AUTO_GENERATE_ALLURE` | false | No | Auto-Allure HTML |

---

## Pytest Markers

| Marker | Usage |
|--------|-------|
| `@TC1`–`@TC99` | Individual test case IDs |
| `@ui` | UI/E2E tests |
| `@api` | API CRUD tests |
| `@regression` | Full regression suite |
| `@login` | Login tests |
| `@signup` | Sign-up tests |
| `@products` | Products tests |
| `@checkout` | Checkout flow |
| `@payment` | Payment tests |
| `@positive_testing` | Happy path |
| `@negative_testing` | Error/edge cases |
| `@security` | XSS, SQLi, auth tests |

---

## DoD (Definition of Done)

- [x] Scenario(s) pass locally
- [x] `pytest --collect-only` passes (no discovery errors)
- [x] No `time.sleep()` or flaky waits introduced
- [x] Report artifacts generated in `test-results/`
- [x] Selectors placed in page objects (not steps)
- [x] Markers/tags updated if needed
- [x] No secrets committed; `.env` remains git-ignored

---

## Reference

- **[AGENTS.md](./AGENTS.md)** — Unified coding guidelines (all platforms)
- **[README.md](./README.md)** — Project overview, setup, execution
- **Platform configs**: [CLAUDE.md](./CLAUDE.md) · [KILO.md](./KILO.md)
- **Rule set**: `.kilo/rules/` and `.claude/rules/` (synchronized copies)
- **Agent guides**: `.claude/agents/` · `.kilo/agent/`
