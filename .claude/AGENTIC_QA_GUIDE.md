# Agentic QA Guide (.claude-style)

Use this guide when running the framework with Claude-style project config.

## 1) Project Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Install browsers: `python -m playwright install --with-deps`
3. Run bootstrap checks:
   - `python .cursor/skills/init/scripts/verify_env.py`
   - `python .cursor/skills/init/scripts/smoke_collect.py`
4. Optional one-command bootstrap (Windows):
   - `./scripts/bootstrap_agentic_qa.ps1`

## 2) Claude Hooks and MCP

- Claude config: `.claude/settings.json`
- Hook scripts: `.claude/hooks/`
- MCP servers included:
  - `playwright-local`
  - `filesystem-project`

Reload your Claude tool session after editing `.claude/settings.json`.

## 3) Claude Command Workflows

- `/feature-development` -> `.claude/commands/feature-development.md`
- `/test-debugging` -> `.claude/commands/test-debugging.md`
- `/agentic-bootstrap` -> `.claude/commands/agentic-bootstrap.md`
- `/agentic-ci-cd` -> `.claude/commands/agentic-ci-cd.md`
- `/generate-test-cases` -> `.claude/commands/generate-test-cases.md`
- `/self-heal-tests` -> `.claude/commands/self-heal-tests.md`
- `/plan-regression-suite` -> `.claude/commands/plan-regression-suite.md`

## 4) Example Agentic Prompts

- "Run `/generate-test-cases` for login + sign-up edge cases."
- "Run `/self-heal-tests` for flaky selectors on login and product flows."
- "Run `/plan-regression-suite` for TC6/TC7 and API smoke."

## 5) CI/CD

- GitHub Actions workflow: `.github/workflows/agentic-qa.yml`
- Jenkins pipeline: `Jenkinsfile`

These pipelines execute init checks and targeted marker runs.

---

## Reference

- **Unified AGENTS.md**: See [AGENTS.md](./AGENTS.md) for all platform guidelines

### Code Style & Rules (All Platforms)

| Platform | Code Style | Testing Rules | Security |
|----------|------------|---------------|----------|
| **Kilo** | [`.kilo/rules/python-coding-style.md`](.kilo/rules/python-coding-style.md) | [`.kilo/rules/common-testing.md`](.kilo/rules/common-testing.md) | [`.kilo/rules/python-security.md`](.kilo/rules/python-security.md) |
| **Claude** | - | [`.claude/rules/test-automation-guardrails.md`](.claude/rules/test-automation-guardrails.md) | - |
| **Cursor** | [`.cursor/rules/python-coding-style.md`](.cursor/rules/python-coding-style.md) | [`.cursor/rules/common-testing.md`](.cursor/rules/common-testing.md) | [`.cursor/rules/python-security.md`](.cursor/rules/python-security.md) |
