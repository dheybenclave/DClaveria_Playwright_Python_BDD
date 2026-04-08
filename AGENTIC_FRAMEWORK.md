# Agentic AI Guide - Test Automation Framework

Centralized guide for ALL AI agents (Cursor, Claude, Kilo, etc.) working with this Playwright Python BDD test automation project.

## Table of Contents
- [Framework Overview](#framework-overview)
- [Project Structure](#project-structure)
- [Required Environment](#required-environment)
- [Test Execution](#test-execution)
- [Framework Rules](#framework-rules)
- [Troubleshooting](#troubleshooting)

---

## Framework Overview

This project uses:
- **Playwright** - Browser automation
- **pytest-bdd** - BDD test framework
- **Python 3.8+** - Programming language

### Key Paths

| Path | Description |
|------|-------------|
| `tests/features` | BDD .feature files (Gherkin) |
| `tests/step_definitions` | Step implementation files |
| `src/pages` | Page Object Models (POM) |
| `utils` | Utility functions |
| `test-results` | Test output/reports |

---

## Required Environment

### Local Setup

```powershell
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install --with-deps

# Verify environment (ALWAYS run this first)
python .cursor/skills/init/scripts/verify_env.py

# Collect tests
python .cursor/skills/init/scripts/smoke_collect.py
```

### Environment Variables

**Required** (in `.env` or CI secrets):
- `BASE_URL` - Target test URL (e.g., https://automationexercise.com)
- `HEADLESS` - true/false for headless mode

**Optional**:
- `RECORD_VIDEO` - Record test videos
- `ADMIN_EMAIL` / `ADMIN_PASSWORD` - Admin credentials
- `LIST_OF_CREDENTIALS` - Test credentials (from GitHub secrets)

---

## Test Execution

### Basic Commands

```bash
# Run all tests
pytest tests/

# Run specific marker
pytest -m "TC6 or TC7" tests/

# Collect tests only
pytest --collect-only -q

# Run with video
HEADLESS=false pytest -m TC6 tests/

# Run parallel (CI)
pytest -n auto --dist loadscope tests/
```

### Test Markers

| Marker | Description |
|--------|-------------|
| `@TC1`, `@TC2`, etc. | Individual test case IDs |
| `@smoke` | Smoke tests |
| `@regression` | Full regression suite |
| `@e2e` | End-to-end tests |

---

## Framework Rules

### 1. NEVER Put Selectors in Step Definitions

**WRONG** ❌:
```python
@when("user clicks login button")
def step_impl(page):
    page.click("#login-btn")  # Selector in step!
```

**CORRECT** ✅:
```python
# Step definition (thin glue)
@when("user clicks login button")
def step_impl(page):
    page.login_page.click_login_button()

# Page object (selectors here)
class LoginPage:
    def click_login_button(self):
        self.page.get_by_role("button", name="Login").click()
```

### 2. ALWAYS Use Page Objects

All selectors MUST be in `src/pages/` directory:
- `src/pages/login_page.py`
- `src/pages/products_page.py`
- `src/pages/checkout_page.py`

Step definitions should only call page object methods.

### 3. Use Semantic Selectors

Prefer these (in order):
```python
# BEST - Semantic, accessible
self.page.get_by_role("button", name="Submit")
self.page.get_by_label("Email")
self.page.get_by_placeholder("Enter email")

# OK - Attribute-based
self.page.locator("[data-testid='submit']")
self.page.locator("[aria-label='Close']")

# AVOID - Fragile selectors
self.page.locator("#submit-button")
self.page.locator("div.card:nth-child(2)")
self.page.locator("text=Submit")
```

### 4. Add Fallback Locators for Resilience

```python
class ProductPage:
    @property
    def add_to_cart_button(self):
        # Primary: semantic selector
        return self.page.get_by_role("button", name="Add to Cart")
    
    def add_to_cart(self):
        try:
            self.add_to_cart_button.click()
        except:
            # Fallback: text-based
            self.page.locator("button", has_text="Add to Cart").click()
```

### 5. Use Explicit Waits

```python
# WRONG ❌ - Fixed sleep
import time
time.sleep(2)

# CORRECT ✅ - Explicit wait
self.page.wait_for_load_state("networkidle")
self.page.wait_for_selector(".product-list")
self.page.get_by_text("Success").wait_for()
```

### 6. Keep Step Definitions Thin

Step definitions should be 1-3 lines maximum:
```python
@when("user logs in with valid credentials")
def step_impl(page):
    page.login_page.login("valid@email.com", "password123")
```

### 7. Use Descriptive Test Markers

Always tag scenarios with `@TC` markers:
```gherkin
@TC6 @smoke
Scenario: User can login with valid credentials
  ...
```

---

## AI Agent Hooks (Optional Automation)

### Available Hooks

This project includes optional hooks for AI sessions:

| Hook | Purpose |
|------|---------|
| `sessionStart` | Show startup checklist |
| `afterFileEdit` | Suggest smoke runs after edits |
| `beforeShellExecution` | Block unsafe git commands |

### Enable Hooks

**For Cursor**: Uses `.cursor/hooks.json`

**For Kilo**: Uses `.kilo/kilo.json` (configured)

**For Claude**: Uses `.claude/` commands

---

## CI/CD Configuration

### GitHub Actions

**Main Workflow**: `.github/workflows/main.yml`

Triggers:
- Push to master
- Pull requests
- Manual dispatch (`workflow_dispatch`)

**Manual Inputs**:
- `run_parallel` - Run tests in parallel
- `test_filter` - Specific marker (e.g., `-m "smoke"`)
- `record_video` - Record test videos

### Environment Verification

The pipeline runs:
```bash
python .cursor/skills/init/scripts/verify_env.py
```

This validates:
- Python version >= 3.8
- Required modules (pytest, playwright, pytest-bdd, dotenv)
- Environment variables (BASE_URL, HEADLESS)

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests fail on CI | Run `verify_env.py` locally first |
| Selector failures | Use semantic selectors, add fallbacks |
| Import errors | Run `pip install -r requirements.txt` |
| No tests collected | Check .feature file syntax |
| Video not recording | Set `RECORD_VIDEO=true` in env |

### Debug Commands

```bash
# Verbose output
pytest -v -m TC6 tests/

# With browser visible
HEADLESS=false pytest -m TC6 tests/

# Single test
pytest -k "test_name" -v tests/
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│  TEST AUTOMATION FRAMEWORK QUICK REFERENCE              │
├─────────────────────────────────────────────────────────┤
│  VERIFY:    python .cursor/skills/init/scripts/verify_env.py
│  COLLECT:   pytest --collect-only -q
│  RUN:       pytest -m "TC6" tests/
│  PARALLEL:  pytest -n auto --dist loadscope tests/
│  VIDEO:     HEADLESS=false pytest -m TC6 tests/
├─────────────────────────────────────────────────────────┤
│  RULES:                                                 │
│  ✗ NO selectors in step definitions                    │
│  ✓ ALL selectors in src/pages/                         │
│  ✓ Use semantic selectors (get_by_role, get_by_label)  │
│  ✓ Add fallback locators for resilience                │
│  ✓ Use explicit waits, NOT time.sleep()               │
│  ✓ Keep step definitions thin (1-3 lines)             │
│  ✓ Always tag scenarios with @TC markers              │
└─────────────────────────────────────────────────────────┘
```

---

## AI Agent Configurations

This project supports multiple AI agents (Cursor, Claude, Kilo). Each has its own configuration folder with commands, agents, hooks, and rules.

### Folder Structure Comparison

| Component | Cursor | Claude | Kilo |
|-----------|--------|--------|------|
| Config | `.cursor/` | `.claude/settings.json` | `.kilo/kilo.json` |
| Commands | `.cursor/skills/init/` | `.claude/commands/` | `.kilo/commands/` |
| Agents | `.cursor/mcp.json` | `.claude/commands/` | `.kilo/agent/` |
| Hooks | `.cursor/hooks/` | `.claude/hooks/` | `.kilo/hooks/` |
| Rules | `.cursor/rules/` | `.claude/rules/` | `.kilo/rules/` |
| Skills | `.cursor/skills/init/` | N/A | `.kilo/skills/init/` |
| Guide | `.cursor/AGENTIC_QA_GUIDE.md` | `.claude/AGENTIC_QA_GUIDE.md` | `.kilo/AGENTIC_QA_GUIDE.md` |

### Quick Agent Selection

**Using Cursor**: Open project in Cursor IDE - hooks and rules auto-apply

**Using Claude**: Prefix prompts with `/` commands from `.claude/commands/`

**Using Kilo**: Use `/verify`, `/collect`, `/test`, `/debug` commands or specialized agents

### Agent-Specific Guides

- [Cursor Guide](./.cursor/AGENTIC_QA_GUIDE.md) - Cursor IDE configuration
- [Claude Guide](./.claude/AGENTIC_QA_GUIDE.md) - Claude CLI commands
- [Kilo Guide](./.kilo/AGENTIC_QA_GUIDE.md) - Kilo CLI configuration

---

## Related Documentation

- [AGENTIC_AI.md](./AGENTIC_AI.md) - Full AI agent guide
- [.cursor/AGENTIC_QA_GUIDE.md](./.cursor/AGENTIC_QA_GUIDE.md) - Cursor-specific
- [.kilo/AGENTS.md](./.kilo/AGENTS.md) - Kilo-specific
