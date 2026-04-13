# Agentic AI Guide - Test Automation Framework

Comprehensive guide for ALL AI agents (Kilo, Cursor, Claude, GitHub Agents) working with this Playwright Python BDD test automation project.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Environment Setup](#environment-setup)
- [Test Execution](#test-execution)
- [AI Agents](#ai-agents)
- [FastMCP Server](#fastmcp-server)
- [Framework Rules](#framework-rules)
- [Hooks](#hooks)
- [CI/CD](#cicd)
- [Troubleshooting](#troubleshooting)

---

## Overview

This project uses multiple AI agent systems:
- **Kilo CLI** (`.kilo/`) - Local AI agent commands and agents
- **Cursor IDE** (`.cursor/`) - IDE with hooks and rules
- **Claude CLI** (`.claude/`) - CLI-based AI commands
- **GitHub Agents** (`.github/agents/`) - Cloud-based agents
- **FastMCP Server** (`.kilo/mcp/`) - MCP protocol for AI test automation

---

## Project Structure

```
.
├── AGENTS.md                    # Agent coding guidelines (root)
├── AGENTIC_GUIDE.md            # This file - unified guide
├── pytest.ini                   # Pytest configuration
├── conftest.py                  # Pytest fixtures
├── .env                         # Environment variables
│
├── .kilo/                       # Kilo CLI Agents
│   ├── agent/                   # Agent definitions
│   ├── command/                 # Slash commands
│   ├── mcp/                     # FastMCP Server
│   ├── hooks/                  # Session hooks
│   ├── rules/                   # AI coding rules
│   └── AGENTS.md               # Kilo-specific config
│
├── .cursor/                     # Cursor IDE
│   ├── hooks/                  # Cursor hooks
│   ├── rules/                  # Cursor rules
│   └── skills/                  # Skills/init scripts
│
├── .claude/                     # Claude CLI
│   ├── hooks/                  # Claude hooks
│   └── commands/               # Claude commands
│
├── .github/                     # GitHub
│   ├── agents/                 # GitHub Agents
│   └── workflows/              # CI/CD pipelines
│
├── tests/
│   ├── features/               # BDD .feature files
│   └── step_definitions/       # Step implementations
│
├── src/pages/                  # Page Object Models
└── utils/                      # Utility functions
```

---

## Environment Setup

### Quick Setup

```powershell
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install --with-deps

# Verify environment (ALWAYS run first)
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
pytest

# Run specific marker (preferred)
pytest -m "TC6 or TC7"

# Run by keyword
pytest -k "login"

# Collect tests only
pytest --collect-only -q

# Run with visible browser
HEADLESS=false pytest -m TC6

# Run parallel (CI)
pytest -n auto --dist loadscope
```

### Via MCP Server

```python
import sys
sys.path.insert(0, '.kilo/mcp')
from server import run_tests_by_marker

result = run_tests_by_marker('TC6')
print(result['stdout'])
```

### Pytest Markers

| Marker | Description |
|--------|-------------|
| `@TC1`, `@TC2`, etc. | Individual test case IDs |
| `@smoke` | Smoke tests |
| `@regression` | Full regression suite |
| `@ui` | UI E2E tests |
| `@api` | API tests |
| `@login` | Login page tests |

---

## AI Agents

### Kilo Agents (`.kilo/agent/`)

| Agent | File | Purpose |
|-------|------|---------|
| Test Planner | `test-planner.md` | Create comprehensive test plans |
| Test Healer | `test-healer.md` | Self-heal failing tests |
| Test Generator | `test-generator.md` | Generate test cases |

**Usage**:
```bash
kilo "Use test-planner for checkout flow"
kilo "Use test-healer to fix selector failures"
kilo "Use test-generator to create login tests"
```

### GitHub Agents (`.github/agents/`)

| Agent | File | Purpose |
|-------|------|---------|
| Playwright Test Planner | `playwright-test-planner.agent.md` | Create test plans via browser |
| Playwright Test Healer | `playwright-test-healer.agent.md` | Fix failing tests |
| Playwright Test Generator | `playwright-test-generator.agent.md` | Generate test cases |

### Kilo Commands (`.kilo/command/`)

| Command | Purpose |
|---------|---------|
| `/verify` | Environment verification |
| `/collect` | Test collection |
| `/test` | Run tests |
| `/debug` | Test debugging |

---

## FastMCP Server

**Location**: `.kilo/mcp/`

MCP (Model Context Protocol) server for AI test automation.

### Available Tools

| Tool | Description |
|------|-------------|
| `run_collect` | Collect all tests without running |
| `run_by_marker` | Run tests by pytest marker |
| `run_by_keyword` | Run tests matching keyword |
| `list_markers` | List available pytest markers |
| `list_features` | List all feature files |
| `run_smoke` | Run smoke/regression tests |

### Installation

```bash
pip install mcp fastmcp
```

---

## Framework Rules

### 1. NEVER Put Selectors in Step Definitions

**WRONG** ❌:
```python
@when("user clicks login button")
def step_impl(page):
    page.click("#login-btn")
```

**CORRECT** ✅:
```python
# Step definition (thin)
@when("user clicks login button")
def step_impl(page):
    page.login_page.click_login_button()

# Page object (selectors here)
class LoginPage:
    def click_login_button(self):
        self.page.get_by_role("button", name="Login").click()
```

### 2. ALWAYS Use Page Objects

All selectors MUST be in `src/pages/`:
- `src/pages/login_page.py`
- `src/pages/products_page.py`
- `src/pages/checkout_page.py`

### 3. Use Semantic Selectors

```python
# BEST - Semantic, accessible
self.page.get_by_role("button", name="Submit")
self.page.get_by_label("Email")
self.page.get_by_placeholder("Enter email")

# GOOD - Attribute-based
self.page.locator("[data-testid='submit']")
self.page.locator("[aria-label='Close']")

# AVOID - Fragile selectors
self.page.locator("#submit-button")
self.page.locator("div.card:nth-child(2)")
```

### 4. Use Explicit Waits

```python
# WRONG ❌
import time
time.sleep(2)

# CORRECT ✅
self.page.wait_for_load_state("networkidle")
self.page.wait_for_selector(".product-list")
self.page.get_by_text("Success").wait_for()
```

### 5. Keep Step Definitions Thin

Step definitions should be 1-3 lines maximum.

### 6. Use Descriptive Test Markers

```gherkin
@TC6 @smoke
Scenario: User can login with valid credentials
```

---

## Hooks

### Kilo Hooks (`.kilo/hooks/`)

| Event | Script | Purpose |
|-------|--------|---------|
| sessionStart | `session_start.py` | Show startup checklist |
| beforePromptSubmit | `before_prompt_submit.py` | Secret detection |
| afterFileEdit | `after_file_edit.py` | Suggest verification |

### Cursor Hooks (`.cursor/hooks/`)

| Event | Script | Purpose |
|-------|--------|---------|
| beforeSubmitPrompt | `before_submit_prompt.py` | Secret detection |
| sessionStart | `session_start.py` | Startup message |
| afterFileEdit | `after_file_edit.py` | Post-edit suggestions |

### Claude Hooks (`.claude/hooks/`)

| Event | Script | Purpose |
|-------|--------|---------|
| pre_tool_use_bash | `pre_tool_use_bash.py` | Block dangerous commands |

---

## CI/CD

### GitHub Actions

**Main Workflow**: `.github/workflows/main.yml`

**Triggers**:
- Push to master
- Pull requests
- Manual dispatch

**Manual Inputs**:
- `run_parallel` - Run tests in parallel
- `test_filter` - Specific marker
- `record_video` - Record test videos

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests fail on CI | Run `verify_env.py` locally first |
| Selector failures | Use semantic selectors, add fallbacks |
| Import errors | Run `pip install -r requirements.txt` |
| No tests collected | Check .feature file syntax |
| Video not recording | Set `HEADLESS=false` |

### Debug Commands

```bash
# Verbose output
pytest -v -m TC6

# With browser visible
HEADLESS=false pytest -m TC6

# Single test
pytest -k "test_name" -v

# Collect only
pytest --collect-only -q
```

---

## Quick Reference

```
┌─────────────────────────────────────────┐
│  TEST AUTOMATION QUICK REFERENCE        │
├─────────────────────────────────────────┤
│  VERIFY:  python verify_env.py         │
│  COLLECT: pytest --collect-only -q      │
│  RUN:     pytest -m "TC6"               │
│  PARALLEL: pytest -n auto                │
│  VIDEO:   HEADLESS=false pytest -m TC6  │
├─────────────────────────────────────────┤
│  RULES:                                  │
│  ✗ NO selectors in step definitions     │
│  ✓ ALL selectors in src/pages/          │
│  ✓ Use semantic selectors              │
│  ✓ Explicit waits (no time.sleep)      │
│  ✓ Keep steps thin (1-3 lines)         │
│  ✓ Tag scenarios with @TC markers      │
└─────────────────────────────────────────┘
```

---

## Related Documentation

- [AGENTS.md](./AGENTS.md) - AI agent coding guidelines
- [.kilo/AGENTS.md](./.kilo/AGENTS.md) - Kilo-specific config
- [.cursor/AGENTIC_QA_GUIDE.md](./.cursor/AGENTIC_QA_GUIDE.md) - Cursor-specific
- [.claude/AGENTIC_QA_GUIDE.md](./.claude/AGENTIC_QA_GUIDE.md) - Claude-specific