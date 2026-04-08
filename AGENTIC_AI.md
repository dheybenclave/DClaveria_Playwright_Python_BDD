# Agentic AI Configuration Guide

Comprehensive guide for using Claude/Cursor AI agents with this Playwright Python BDD project.

## Table of Contents
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Hooks](#hooks)
- [MCP Servers](#mcp-servers)
- [Rules](#rules)
- [GitHub Agents](#github-agents)
- [Commands](#commands)
- [Workflow](#workflow)

---

## Quick Start

### One-Time Setup
```powershell
# Windows - Run bootstrap script
./scripts/bootstrap_agentic_qa.ps1

# Or manual setup
pip install -r requirements.txt
python -m playwright install --with-deps

# Verify environment
python .cursor/skills/init/scripts/verify_env.py
python .cursor/skills/init/scripts/smoke_collect.py
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

## Project Structure

```
.
├── .cursor/
│   ├── hooks/           # AI hook scripts
│   │   ├── session_start.py
│   │   ├── before_shell_execution.py
│   │   ├── after_shell_execution.py
│   │   ├── after_file_edit.py
│   │   └── before_submit_prompt.py
│   ├── hooks.json      # Hook configuration
│   ├── mcp.json        # MCP server configuration
│   ├── rules/          # AI coding rules
│   │   ├── playwright-python-framework.md
│   │   ├── python-testing.md
│   │   ├── python-security.md
│   │   └── common-testing.md
│   ├── skills/init/
│   │   └── scripts/
│   │       ├── verify_env.py      # Environment verification
│   │       └── smoke_collect.py   # Test collection check
│   └── AGENTIC_QA_GUIDE.md        # Full QA guide
├── .github/
│   ├── workflows/      # CI/CD pipelines
│   └── agents/        # GitHub agents
├── tests/
│   ├── features/     # BDD feature files
│   └── step_definitions/  # Step implementations
├── src/pages/         # Page object models
└── utils/             # Utilities
```

---

## Hooks

Hooks are defined in `.cursor/hooks.json` and automate tasks during AI sessions.

### Hook Configuration

| Event | Script | Purpose |
|-------|--------|---------|
| `sessionStart` | `session_start.py` | Show startup checklist |
| `beforeShellExecution` | `before_shell_execution.py` | Block unsafe git commands |
| `afterShellExecution` | `after_shell_execution.py` | Remind verification commands |
| `afterFileEdit` | `after_file_edit.py` | Suggest smoke collection runs |
| `beforeSubmitPrompt` | `before_submit_prompt.py` | Warn about secret patterns |

### Hook Scripts

**session_start.py** - Runs on AI session start:
```python
print(
    "[QA Agentic] Session start checklist: "
    "1) python .cursor/skills/init/scripts/verify_env.py "
    "2) python .cursor/skills/init/scripts/smoke_collect.py "
    "3) use .cursor/AGENTIC_QA_GUIDE.md for workflows."
)
```

**before_shell_execution.py** - Blocks destructive git commands:
- Prevents `git push --force`
- Warns on hard resets
- Blocks dangerous operations

**after_shell_execution.py** - Post-shell reminders:
- Suggests verification commands
- Reminds about test runs

**after_file_edit.py** - After code edits:
```python
print(
    "[QA Agentic] File edited. Suggested quick checks: "
    "`python .cursor/skills/init/scripts/smoke_collect.py` "
    "and rerun the affected test marker."
)
```

**before_submit_prompt.py** - Secret detection:
- Scans for API keys, tokens, passwords
- Warns before sending prompts externally

---

## MCP Servers

MCP (Model Context Protocol) servers extend AI capabilities. Configured in `.cursor/mcp.json`.

### Available MCP Servers

| Server | Command | Purpose |
|--------|---------|---------|
| `playwright-local` | `npx @playwright/mcp@latest` | Local browser automation |
| `filesystem-project` | `npx @modelcontextprotocol/server-filesystem .` | Project filesystem access |

### MCP Configuration
```json
{
  "mcpServers": {
    "playwright-local": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {
        "PLAYWRIGHT_BROWSERS_PATH": "0"
      }
    },
    "filesystem-project": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

### Using MCP Tools
After adding/changing MCP config:
1. Reload Cursor window
2. Verify MCP servers appear in available tools
3. Use `npx` in terminal if issues arise

---

## Rules

AI rules define coding standards. Located in `.cursor/rules/`.

### Available Rules

| Rule File | Description |
|-----------|-------------|
| `playwright-python-framework.md` | Framework conventions & workflow |
| `python-testing.md` | Python testing best practices |
| `python-security.md` | Security guidelines |
| `python-coding-style.md` | Code style conventions |
| `common-testing.md` | General testing guidelines |

### Key Framework Conventions

From `playwright-python-framework.md`:
- **Features**: `tests/features`
- **Steps**: `tests/step_definitions`
- **Pages**: `src/pages`
- **Utilities**: `utils`
- **Artifacts**: `test-results`

**Reliability Guardrails**:
- Do not put selectors directly in step definition files
- Keep waits centralized and deterministic
- Preserve existing marker naming and report output paths

---

## GitHub Agents

Located in `.github/agents/`. Specialized AI agents for specific tasks.

### Available Agents

| Agent | Purpose |
|-------|---------|
| `playwright-test-planner.agent.md` | Create comprehensive test plans |
| `playwright-test-healer.agent.md` | Self-heal failing tests |
| `playwright-test-generator.agent.md` | Generate test cases |

### playwright-test-planner

Use for creating test plans:
- Navigate and explore web applications
- Analyze user flows
- Design comprehensive test scenarios
- Output as markdown test plan

**Tools Available**:
- browser_navigate, browser_click, browser_type
- browser_screenshot, browser_snapshot
- planner_setup_page, planner_save_plan

---

## Commands

Slash commands for common tasks. Located in `.claude/commands/`.

| Command | Purpose |
|---------|---------|
| `/test-debugging` | Debug failing tests |
| `/self-heal-tests` | Fix flaky selectors |
| `/plan-regression-suite` | Plan regression test suite |
| `/generate-test-cases` | Generate test cases from requirements |
| `/feature-development` | Add new scenarios |
| `/agentic-ci-cd` | CI/CD integration help |
| `/agentic-bootstrap` | Initial project setup |

---

## Workflow

### Daily QA Agentic Workflow

```bash
# 1. Initialize session
python .cursor/skills/init/scripts/verify_env.py

# 2. Collect tests quickly
pytest --collect-only -q

# 3. Run targeted scenario/tag
pytest -m "TC6 or TC7" -q

# 4. Ask AI for help with:
#    - Feature to step mapping
#    - Selector stability
#    - Flaky test triage

# 5. Before finalizing
#    - Rerun targeted tests
#    - Rerun collect-only check
#    - Inspect reports in test-results/reports
```

### Running Tests

```bash
# All tests
pytest

# Specific marker
pytest -m "TC6 or TC7"

# Collection check
pytest --collect-only

# With video recording
HEADLESS=false pytest -m TC6

# Parallel execution (CI)
pytest -n auto --dist loadscope tests/
```

---

## CI/CD Integration

### GitHub Actions

**Workflow**: `.github/workflows/main.yml`

**Triggers**:
- Push to master
- Pull requests to master
- Manual dispatch (workflow_dispatch)

**Manual Inputs**:
- `run_parallel`: Run tests in parallel?
- `test_filter`: Specific test filter (e.g., `-m "smoke"`)
- `record_video`: Record test videos?

**Environment Variables**:
- `BASE_URL`: Target test URL
- `HEADLESS`: Run in headless mode
- `RECORD_VIDEO`: Enable video recording
- `LIST_OF_CREDENTIALS`: Test credentials (from secrets)

### Agentic QA Workflow

**Workflow**: `.github/workflows/agentic-qa.yml`

Includes:
- Dependency installation
- Playwright browser install
- Agentic init checks (`verify_env.py`, `smoke_collect.py`)
- Targeted marker execution
- Artifact upload

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP tools don't appear | Verify `.cursor/mcp.json` syntax, restart Cursor |
| Hooks don't run | Check `.cursor/hooks.json` syntax, verify Python available |
| Tests fail on CI | Run `verify_env.py` locally first |
| Selector failures | Use `/test-debugging` command |

---

## Recommended AI Prompts

### Test Generation
> "Create pytest-bdd scenarios for: user can login, invalid password message, and locked account flow. Add `.feature` outline examples and thin step definitions mapped to existing page objects."

### Self-Healing
> "Analyze this failing Playwright selector and propose self-healing fallback locator strategy in the page object only, with no step-definition locator changes."

### Test Planning
> "Plan a regression suite for checkout guest vs logged-in users with markers, feature files, step reuse matrix, and execution order."

### Feature Development
> "Apply `/feature-development` to add a new scenario with minimal step logic."

---

## Additional Resources

- [Full QA Guide](./.cursor/AGENTIC_QA_GUIDE.md)
- [Framework Rules](./.cursor/rules/playwright-python-framework.md)
- [MCP JSON](./.cursor/mcp.json)
- [Hooks JSON](./.cursor/hooks.json)
