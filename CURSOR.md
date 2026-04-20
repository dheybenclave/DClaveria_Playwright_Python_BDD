# CURSOR.md - Cursor AI Agent Configuration

This document provides Cursor-specific configuration for AI agents in this Playwright Python BDD test automation project.

---

## MCP Configuration

**File**: `.cursor/mcp.json`

```json
{
  "mcpServers": {
    "playwright-local": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": { "PLAYWRIGHT_BROWSERS_PATH": "0" }
    },
    "filesystem-project": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."]
    }
  }
}
```

---

## Hooks Configuration

**File**: `.cursor/hooks.json`

| Hook | File | Description |
|------|------|-------------|
| sessionStart | `.cursor/hooks/session_start.py` | Show QA agentic startup checklist |
| beforeShellExecution | `.cursor/hooks/before_shell_execution.py` | Block unsafe git commands |
| afterShellExecution | `.cursor/hooks/after_shell_execution.py` | Remind quick verification |
| afterFileEdit | `.cursor/hooks/after_file_edit.py` | Remind collection smoke |
| beforeSubmitPrompt | `.cursor/hooks/before_submit_prompt.py` | Warn about secret tokens |

### Session Start Hook

```bash
python .cursor/skills/init/scripts/verify_env.py
python .cursor/skills/init/scripts/smoke_collect.py
```

### Before Submit Prompt

Detects common secret patterns:
- OpenAI API keys (`sk-...`)
- GitHub tokens (`ghp_...`)
- AWS keys (`AKIA...`)

---

## Rules

**Directory**: `.cursor/rules/`

All rules are synced with Claude and Kilo:

| Rule | Description |
|------|-------------|
| `common-testing.md` | Testing requirements and stability rules |
| `python-coding-style.md` | Python code style (PEP 8, type hints) |
| `python-security.md` | Security best practices |
| `python-testing.md` | Pytest and BDD guidance (Cursor-specific) |
| `playwright-python-framework.md` | Framework workflow conventions |
| `test-automation-guardrails.md` | Core test automation guardrails |

---

## Skills

**Directory**: `.cursor/skills/init/`

- `SKILL.md` - Environment initialization skill
- `scripts/verify_env.py` - Environment verification script
- `scripts/smoke_collect.py` - Test collection script

---

## Key Paths

| Path | Description |
|------|-------------|
| `tests/features` | BDD feature files |
| `tests/step_definitions` | Step implementations |
| `src/pages` | Page object models |
| `.cursor/rules/` | Cursor-specific coding rules |
| `.cursor/hooks/` | Cursor hook scripts |
| `.cursor/mcp.json` | MCP server configuration |
| `.cursor/skills/` | Cursor skills for initialization |

---

## Commands

Cursor uses slash commands from the main AGENTS.md:

- `/feature-development` — Add new feature files and corresponding steps
- `/test-debugging` — Triage failing tests
- `/self-heal-tests` — Fix flaky selectors with locator fallbacks
- `/generate-test-cases` — Generate tests from requirements
- `/plan-regression-suite` — Plan marker-based regression suites

---

## Environment Variables

**Required**:
- `BASE_URL` - Target application URL
- `HEADLESS` - Run browser in headless mode

**Optional**:
- `RECORD_VIDEO` - Record test videos
- `ADMIN_EMAIL` / `ADMIN_PASSWORD` - Admin credentials
- `AUTO_GENERATE_ALLURE` - Enable Allure reporting

---

## Reference

- **Unified AGENTS.md**: See [AGENTS.md](./AGENTS.md) for all platform guidelines
- **Kilo config**: [`.kilo/kilo.json`](.kilo/kilo.json)
- **Claude config**: [`.claude/settings.json`](.claude/settings.json)
- **Agentic QA Guide**: [`.cursor/AGENTIC_QA_GUIDE.md`](.cursor/AGENTIC_QA_GUIDE.md)