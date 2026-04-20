# KILO.md - Kilo AI Agent Configuration

This document provides Kilo-specific configuration for AI agents in this Playwright Python BDD test automation project.

## Project Configuration

**Config File**: `.kilo/kilo.json`

```json
{
  "model": "kilo/minimax/minimax-m2.1:free",
  "permission": { "bash": "allow" }
}
```

---

## Commands

### 1. verify - Environment Verification

**File**: `.kilo/command/verify.md`

Verify environment setup:
- Check Python version
- Verify required modules
- Validate .env configuration

**Usage**:
```bash
kilo "Verify environment setup"
```

### 2. collect - Test Collection

**File**: `.kilo/command/collect.md`

Collect and list test cases:
- List all BDD scenarios
- Show test markers
- Display test coverage

**Usage**:
```bash
kilo "Collect all test cases"
```

### 3. debug - Test Debugging

**File**: `.kilo/command/debug.md`

Debug failing tests:
- Analyze failure causes
- Suggest fixes
- Provide debugging tips

**Usage**:
```bash
kilo "Debug failing test TC6"
```

### 4. test - Run Tests

**File**: `.kilo/command/test.md`

Run pytest tests:
- Execute specific markers
- Run parallel tests
- Generate reports

**Usage**:
```bash
kilo "Run tests with marker TC6"
```

---

## Available Agents

### 1. Test Executor Agent

**File**: `.kilo/agent/test-executor.md`

Use for test execution:
- Run smoke, regression, and E2E tests
- Execute API and security tests
- Analyze test results and report findings

### 2. Test Architect Agent

**File**: `.kilo/agent/test-architect.md`

Use for framework architecture:
- Design and review page objects
- Analyze test structure
- Define coding standards

### 3. Product Owner Agent

**File**: `.kilo/agent/product-owner.md`

Use for requirements analysis:
- Break down user stories
- Define acceptance criteria
- Create testable scenarios

### 4. Scrum Master Agent

**File**: `.kilo/agent/scrum-master.md`

Use for team coordination:
- Plan test sprints
- Coordinate between roles
- Track progress and remove blockers

### 5. Test Planner Agent

**File**: `.kilo/agent/test-planner.md`

Use for test planning:
- Navigate and explore web applications
- Analyze user flows
- Design comprehensive test scenarios

### 6. Test Healer Agent

**File**: `.kilo/agent/test-healer.md`

Use for fixing failing tests:
- Analyze selector failures
- Propose self-healing locator strategies
- Fix flaky tests

### 7. Test Generator Agent

**File**: `.kilo/agent/test-generator.md`

Use for generating test cases:
- Create BDD scenarios from requirements
- Generate step definitions
- Create page object models

---

> **Note**: The first 4 agents (test-executor, test-architect, product-owner, scrum-master) mirror the Claude agents in `.claude/agents/`. The last 3 (test-planner, test-healer, test-generator) are Kilo-specific.

---

## FastMCP Test Server

**Location**: `.kilo/mcp/fastmcp_server.py`

MCP (Model Context Protocol) server that provides AI-powered test automation tools.

### Available Tools

| Tool | Description |
|------|-------------|
| `run_collect` | Collect all tests without running |
| `run_by_marker` | Run tests by pytest marker (TC6, regression, api, ui) |
| `run_by_keyword` | Run tests matching keyword in name |
| `list_markers` | List available pytest markers |
| `list_features` | List all feature files |
| `run_smoke` | Run smoke/regression tests |

### Usage

```python
import sys
sys.path.insert(0, '.kilo/mcp')
from server import run_tests_by_marker, collect_tests

# Run tests by marker
result = run_tests_by_marker('TC6')
print(result['stdout'])

# Collect all tests
result = collect_tests()
```

---

## Hooks

### Session Start

**File**: `.kilo/hooks/session_start.py`

Shows Kilo QA agentic startup checklist:
```bash
python .kilo/skills/init/scripts/verify_env.py
python .kilo/skills/init/scripts/smoke_collect.py
```

### Before Prompt Submit

**File**: `.kilo/hooks/before_prompt_submit.py`

Validates prompts for secrets before submission. Detects:
- OpenAI API keys (`sk-...`)
- GitHub tokens (`ghp_...`)
- AWS keys (`AKIA...`)

### After File Edit

**File**: `.kilo/hooks/after_file_edit.py`

Reminds quick checks after file edits:
```bash
python .kilo/skills/init/scripts/smoke_collect.py
```

---

## MCP Configuration

**File**: `.kilo/kilo.json`

```json
{
  "mcp": {
    "playwright": {
      "type": "local",
      "command": ["npx", "-y", "@playwright/mcp@0.0.38"]
    }
  }
}
```

---

## Key Paths

| Path | Description |
|------|-------------|
| `tests/features` | BDD feature files |
| `tests/step_definitions` | Step implementations |
| `src/pages` | Page object models |
| `utils` | Utility functions |
| `test-results` | Test artifacts |
| `.kilo/mcp` | FastMCP server for AI test automation |
| `.kilo/command/` | Kilo CLI commands |
| `.kilo/agent/` | Kilo AI agents |
| `.kilo/rules/` | Kilo-specific rules |
| `.kilo/hooks/` | Kilo hook scripts |

---

## Environment Variables

**Required**:
- `BASE_URL` - Target application URL
- `HEADLESS` - Run browser in headless mode

**Optional**:
- `RECORD_VIDEO` - Record test videos
- `ADMIN_EMAIL` / `ADMIN_PASSWORD` - Admin credentials
- `LIST_OF_CREDENTIALS` - Test credentials from secrets
- `AUTO_GENERATE_ALLURE` - Enable Allure reporting (default: false)

---

## Reference

- **Unified AGENTS.md**: See [AGENTS.md](./AGENTS.md) for all platform guidelines
- **Claude config**: [`.claude/settings.json`](.claude/settings.json)
- **Cursor config**: [`.cursor/hooks.json`](.cursor/hooks.json)