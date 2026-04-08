# Kilo AI Agents Configuration

This document defines the AI agents and commands available for Kilo CLI in this Playwright Python BDD project.

## Table of Contents
- [Project Configuration](#project-configuration)
- [Available Agents](#available-agents)
- [Commands](#commands)
- [Usage](#usage)

---

## Project Configuration

**Config File**: `.kilo/kilo.json`

```json
{
  "model": "kilo/minimax/minimax-m2.1:free",
  "permission": { "bash": "allow" }
}
```

### Key Paths

| Path | Description |
|------|-------------|
| `tests/features` | BDD feature files |
| `tests/step_definitions` | Step implementations |
| `src/pages` | Page object models |
| `utils` | Utility functions |
| `test-results` | Test artifacts |

---

## Available Agents

### 1. Test Planner Agent

**File**: `.kilo/agent/test-planner.md`

Use for creating comprehensive test plans:
- Navigate and explore web applications
- Analyze user flows
- Design comprehensive test scenarios
- Output as markdown test plan

**When to use**:
- Planning new test suites
- Analyzing application functionality
- Creating regression test plans

### 2. Test Healer Agent

**File**: `.kilo/agent/test-healer.md`

Use for fixing failing tests:
- Analyze selector failures
- Propose self-healing locator strategies
- Fix flaky tests

**When to use**:
- Test failures due to selector changes
- Flaky test triage
- Selector stability issues

### 3. Test Generator Agent

**File**: `.kilo/agent/test-generator.md`

Use for generating test cases:
- Create BDD scenarios from requirements
- Generate step definitions
- Create page object models

**When to use**:
- Adding new features to test
- Generating test cases from user stories
- Expanding test coverage

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

## Framework Conventions

### Reliability Guardrails

- Do not put selectors directly in step definition files
- Keep waits centralized and deterministic
- Preserve existing marker naming and report output paths
- Use page objects for all selectors

### Test Structure

```
tests/
├── features/           # .feature files (Gherkin)
│   └── e2e_suites/
├── step_definitions/   # Python step implementations
└── reports/            # Test reports

src/
└── pages/              # Page object models

test-results/          # Pytest output
```

### Environment Variables

**Required**:
- `BASE_URL` - Target application URL
- `HEADLESS` - Run browser in headless mode

**Optional**:
- `RECORD_VIDEO` - Record test videos
- `ADMIN_EMAIL` / `ADMIN_PASSWORD` - Admin credentials
- `LIST_OF_CREDENTIALS` - Test credentials from secrets

---

## Quick Start

### One-Time Setup

```powershell
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install --with-deps

# Verify environment
python .cursor/skills/init/scripts/verify_env.py
```

### Daily Workflow

```bash
# 1. Verify environment
python .cursor/skills/init/scripts/verify_env.py

# 2. Collect tests
pytest --collect-only -q

# 3. Run targeted tests
pytest -m "TC6 or TC7" -q

# 4. Run with video
HEADLESS=false pytest -m TC6
```

---

## CI/CD Integration

### GitHub Actions

**Main Workflow**: `.github/workflows/main.yml`

**Triggers**:
- Push to master
- Pull requests
- Manual dispatch with inputs:
  - `run_parallel` - Run tests in parallel
  - `test_filter` - Specific test filter
  - `record_video` - Record test videos

### Agentic QA Workflow

**File**: `.github/workflows/agentic-qa.yml`

Includes:
- Dependency installation
- Playwright browser install
- Environment verification
- Test execution
- Artifact upload

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests fail on CI | Run verify_env.py locally first |
| Selector failures | Use debug command |
| Environment issues | Check .env file and environment variables |

---

## Related Documentation

- [Full AI Agent Guide](../AGENTIC_AI.md)
- [Cursor Configuration](../.cursor/AGENTIC_QA_GUIDE.md)
- [GitHub Agents](../.github/agents/)
