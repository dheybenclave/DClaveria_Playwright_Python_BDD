# Agentic QA Guide (Project Local)

This guide explains how QA engineers can use AI agents safely and consistently
in this Playwright Python BDD framework.

## 1) One-Time Setup

1. Open the project in Cursor.
2. Ensure Python dependencies are installed:
   - `pip install -r requirements.txt`
3. Install Playwright browsers:
   - `python -m playwright install --with-deps`
   - If unsupported, use `python -m playwright install`
4. Confirm local environment readiness:
   - `python .cursor/skills/init/scripts/verify_env.py`
   - `python .cursor/skills/init/scripts/smoke_collect.py`
5. One-command bootstrap (Windows PowerShell):
   - `./scripts/bootstrap_agentic_qa.ps1`

## 2) Enable Project Hook Automation

- Project hook config is at `.cursor/hooks.json`.
- Hook scripts are in `.cursor/hooks/`.
- These hooks:
  - show startup reminders,
  - block risky git operations,
  - remind verification commands after edits/shell steps,
  - warn if prompt text appears to contain secrets.

## 3) Enable MCP Servers for Agentic Work

Project MCP config is at `.cursor/mcp.json`.

Included servers:
- `playwright-local`: local browser automation MCP via Playwright.
- `filesystem-project`: project filesystem MCP (scoped to repo).

After adding/changing MCP config, reload Cursor window and confirm MCP servers
are available in the project.

## 4) Daily QA Agentic Workflow

1. Initialize session:
   - `python .cursor/skills/init/scripts/verify_env.py`
2. Collect tests quickly:
   - `pytest --collect-only -q`
3. Run a targeted scenario/tag:
   - `pytest -m "TC6 or TC7" -q`
4. Ask AI to help with:
   - feature to step mapping (`tests/features` -> `tests/step_definitions`)
   - selector stability in page objects (`src/pages`)
   - flaky test triage and retry strategy
5. Before finalizing:
   - rerun targeted tests
   - rerun collect-only check
   - inspect report artifacts in `test-results/reports`

## 5) Recommended Prompts for QA

- "Use `/test-debugging` on this failing marker and suggest root cause."
- "Apply `/feature-development` to add a new scenario with minimal step logic."
- "Refactor selector handling into page objects and keep steps declarative."

## 6) Agentic AI Examples for QA

### A) Auto-generate test cases from requirement text

Prompt example:
- "Create pytest-bdd scenarios for: user can login, invalid password message, and locked account flow. Add `.feature` outline examples and thin step definitions mapped to existing page objects."

Expected output shape:
- new feature file under `tests/features/regression_suites/`
- minimal step glue in `tests/step_definitions/`
- page object reuse in `src/pages/`

### B) Self-healing triage for flaky selectors

Prompt example:
- "Analyze this failing Playwright selector and propose self-healing fallback locator strategy in the page object only, with no step-definition locator changes."

Expected output shape:
- locator fallback strategy (`get_by_role` -> text/attribute fallback)
- deterministic wait/assert update
- short risk note for false-positive matches

### C) Planning a new regression suite

Prompt example:
- "Plan a regression suite for checkout guest vs logged-in users with markers, feature files, step reuse matrix, and execution order."

Expected output shape:
- phased test plan
- marker strategy (`@TC#`, `@e2e`)
- reusable step/page mapping
- smoke vs full regression split

## 7) CI/CD Agentic Integration

### GitHub Actions

- Workflow file: `.github/workflows/agentic-qa.yml`
- Includes:
  - dependency install
  - Playwright browser install
  - agentic init checks (`verify_env.py`, `smoke_collect.py`)
  - targeted marker execution
  - artifact upload

### Jenkins

- Pipeline file: `Jenkinsfile`
- Includes:
  - checkout + Python setup
  - Playwright browser install
  - agentic init checks
  - optional targeted marker run via parameter (`PYTEST_MARKER`)
  - test artifact archival

## 8) Troubleshooting

- If MCP tools do not appear:
  - verify `.cursor/mcp.json` syntax,
  - restart Cursor,
  - verify `npx` is available in terminal.
- If hooks do not run:
  - verify `.cursor/hooks.json` syntax,
  - check Python is available as `python`,
  - run hook scripts directly to validate.

## 9) Migration Scope Note

This project uses a curated migration from Everything Claude Code for Python
Playwright QA workflows. JavaScript/Node-heavy parts from the source repo were
not copied blindly to avoid runtime conflicts in this Python framework.

---

## Reference

- **Unified AGENTS.md**: See [AGENTS.md](./AGENTS.md) for all platform guidelines

### Code Style & Rules (All Platforms)

| Platform | Code Style | Testing Rules | Security |
|----------|------------|---------------|----------|
| **Kilo** | [`.kilo/rules/python-coding-style.md`](.kilo/rules/python-coding-style.md) | [`.kilo/rules/common-testing.md`](.kilo/rules/common-testing.md) | [`.kilo/rules/python-security.md`](.kilo/rules/python-security.md) |
| **Claude** | [`.claude/rules/*.md`](.claude/rules/test-automation-guardrails.md) | - | - |
| **Cursor** | [`.cursor/rules/python-coding-style.md`](.cursor/rules/python-coding-style.md) | [`.cursor/rules/common-testing.md`](.cursor/rules/common-testing.md) | [`.cursor/rules/python-security.md`](.cursor/rules/python-security.md) |
