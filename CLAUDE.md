# CLAUDE.md - Claude AI Agent Configuration

This document provides Claude-specific configuration for AI agents in this Playwright Python BDD test automation project.

---

## Settings Configuration

**File**: `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [{ "command": "python .claude/hooks/session_start.py" }],
    "PreToolUse": [{ "matcher": "Bash", "command": "python .claude/hooks/pre_tool_use_bash.py" }],
    "PostToolUse": [
      { "matcher": "Edit|Write|MultiEdit", "command": "python .claude/hooks/post_tool_use_edit.py" },
      { "matcher": "Bash", "command": "python .claude/hooks/post_tool_use_bash.py" }
    ],
    "UserPromptSubmit": [{ "command": "python .claude/hooks/user_prompt_submit.py" }]
  },
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

## Hooks

| Hook | File | Description |
|------|------|-------------|
| SessionStart | `.claude/hooks/session_start.py` | Show startup checklist |
| PreToolUse (Bash) | `.claude/hooks/pre_tool_use_bash.py` | Pre-execution bash checks |
| PostToolUse (Edit/Write) | `.claude/hooks/post_tool_use_edit.py` | Post-edit reminders |
| PostToolUse (Bash) | `.claude/hooks/post_tool_use_bash.py` | Post-shell reminders |
| UserPromptSubmit | `.claude/hooks/user_prompt_submit.py` | Prompt secret validation |

### Session Start Hook

Shows startup checklist:
```bash
python .claude/hooks/session_start.py
```

---

## Commands

**Directory**: `.claude/commands/`

Claude has the most comprehensive command set:

| Command | File | Description |
|---------|------|-------------|
| feature-development | `.claude/commands/feature-development.md` | Add new feature files and steps |
| test-debugging | `.claude/commands/test-debugging.md` | Triage failing tests |
| self-heal-tests | `.claude/commands/self-heal-tests.md` | Fix flaky selectors |
| generate-test-cases | `.claude/commands/generate-test-cases.md` | Generate tests from requirements |
| plan-regression-suite | `.claude/commands/plan-regression-suite.md` | Plan marker-based regression |
| agentic-ci-cd | `.claude/commands/agentic-ci-cd.md` | CI/CD automation |
| agentic-bootstrap | `.claude/commands/agentic-bootstrap.md` | Project bootstrap |

---

## Agents

**Directory**: `.claude/agents/`

| Agent | File | Description |
|-------|------|-------------|
| qa-test-automation-engineer | `.claude/agents/qa-test-automation-engineer.md` | QA automation specialist |
| test-architect | `.claude/agents/test-architect.md` | Test architecture design |
| product-owner-business-analyst | `.claude/agents/product-owner-business-analyst.md` | Requirements analysis |
| scrum-team-leader | `.claude/agents/scrum-team-leader.md` | Project management |

---

## Rules

**Directory**: `.claude/rules/`

All rules are synced with Cursor and Kilo:

| Rule | Description |
|------|-------------|
| `common-testing.md` | Testing requirements and stability rules |
| `python-coding-style.md` | Python code style (PEP 8, type hints) |
| `python-security.md` | Security best practices |
| `playwright-python-framework.md` | Framework workflow conventions |
| `test-automation-guardrails.md` | Core test automation guardrails |

---

## Key Paths

| Path | Description |
|------|-------------|
| `tests/features` | BDD feature files |
| `tests/step_definitions` | Step implementations |
| `src/pages` | Page object models |
| `.claude/settings.json` | Claude settings and hooks |
| `.claude/commands/` | Claude-specific commands |
| `.claude/agents/` | Claude AI agents |
| `.claude/hooks/` | Claude hook scripts |
| `.claude/rules/` | Claude-specific rules |

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
- **Cursor config**: [`.cursor/hooks.json`](.cursor/hooks.json)
- **Agentic QA Guide**: [`.claude/AGENTIC_QA_GUIDE.md`](.claude/AGENTIC_QA_GUIDE.md)