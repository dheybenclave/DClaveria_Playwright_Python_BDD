# Test Automation Guardrails

## Core Principles

- **Thin steps, rich pages**: Step definitions delegate all UI operations and assertions to page objects
- **Selectors belong in page objects**: Never put CSS/XPath selectors directly in step definitions
- **No time.sleep()**: Use deterministic waits only (`page.wait_for_load_state()`, `expect(locator).to_be_visible()`)
- **Keep steps declarative**: Step definitions should be 1–3 lines maximum

## Selector Strategy

### Semantic First

```python
# ✅ BEST — Playwright built-in locators (auto-waiting, resilient)
self.page.get_by_role("button", name="Add to cart")
self.page.get_by_label("Email address")
self.page.get_by_placeholder("Enter your email")
self.page.get_by_text("Welcome, User")
```

### Data Attributes

```python
# ✅ GOOD — Custom data attributes for complex elements
self.page.locator("[data-qa='product-add-to-cart']")
self.page.locator("[data-testid='login-submit']")
```

### Avoid Brittle Selectors

```python
# ❌ AVOID — Fragile CSS
self.page.locator("#submit-button")           # ID may change
self.page.locator("div.container > div:nth-child(2)")  # Layout-dependent
```

## Wait Strategy

### Always Use Explicit Waits

```python
# ❌ WRONG
import time
time.sleep(2)

# ✅ CORRECT
self.page.wait_for_load_state("networkidle")
expect(self.lbl_confirmation).to_be_visible(timeout=10000)
self.btn_submit.wait_for(state="attached")
```

### Page-Level Wait Hooks

Define common wait patterns in `BasePage`:

```python
class UIBasePage:
    def wait_for_page_load(self):
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_load_state("networkidle")
```

## BDD Discipline

- Write scenarios in Gherkin: `Given/When/Then` with clear business language
- Avoid technical jargon in `.feature` files
- One action per step
- Use scenario outlines (`Examples:`) for data-driven tests
- Use descriptive scenario names (verb-first imperatives)
- Use json for test data for each test cases

```gherkin
@TC6 @positive_testing @login
Scenario: User can login with valid credentials
    Given the user is on the /login page
    When they enter valid credentials for role "standard_user"
    And they click the login button
    Then they should be redirected to the dashboard
```

## Test Data Management

- Use `test_datas/` directory for JSON/CSV fixtures
- Load via `utils.config.Config.get_test_data()`
- Never hardcode test data in page objects or steps

## Reporting Requirements

- Ensure `test-results/` contains:
  - `report.html` (pytest-html)
  - `screenshots/` (on failure)
  - `videos/` (if `RECORD_VIDEO=true`)
- Allure results go to `allure-results/` (auto-generated `allure-report/`)

## Validation Before Completion

Run **in order**:

1. **Targeted test** — `pytest -m TC6` (fastest feedback)
2. **Collection check** — `pytest --collect-only` (discovery integrity)
3. **Regression sweep** — `pytest -m regression` or related tags

If any step fails, fix before proceeding.

## Documentation Discipline

- Keep feature files readable by non-technical stakeholders
- Ensure scenario names are unique and imperative ("User can...", "System shows...")
- Update `README.md`, `AGENTS.md`, and platform-specific docs when workflow conventions change
- Sync rule files across `.kilo/rules/`, `.cursor/rules/`, `.claude/rules/` after any modification

## No-No List (Never Do)

| Practice | Why It's Bad | Alternative |
|----------|--------------|-------------|
| `time.sleep()` | Unreliable, slows suite | Use `expect(locator).to_be_visible(timeout=5000)` |
| Hardcoded credentials | Security risk | Load from `.env` via `Config` |
| Inline selectors in steps | Brittle, hard to maintain | Page object properties |
| Long step definitions (>3 lines) | Hard to read/debug | Move logic to page objects |
| Ambiguous scenario names | Poor traceability | Use clear imperative statements |
| Missing `@TC#` markers | Cannot target runs | Add unique test case IDs |
| Committing `.env` values | Secret leakage | Add to `.gitignore` |
| Skipping `--collect-only` | Undetected discovery issues | Run before every commit |

---

**Related:** See `common-testing.md` for the Definition of Done checklist and validation sequence.
