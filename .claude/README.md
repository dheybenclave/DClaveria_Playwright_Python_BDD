# Claude Configuration (Migrated and Adapted)

This folder contains a curated migration of agentic guidance from
`D:/Automation/Claude/everything-claude-code`, adapted for this Python
Playwright BDD automation framework.

## Included

- `.claude/rules/test-automation-guardrails.md`
- `.claude/commands/feature-development.md`
- `.claude/commands/test-debugging.md`
- `.claude/settings.json` (hooks + MCP for project-local Claude-style runtime)
- `.claude/hooks/` (safety and QA reminders)
- `.claude/commands/agentic-bootstrap.md`
- `.claude/commands/agentic-ci-cd.md`
- `.claude/commands/generate-test-cases.md`
- `.claude/commands/self-heal-tests.md`
- `.claude/commands/plan-regression-suite.md`
- `.claude/AGENTIC_QA_GUIDE.md`

## Notes

- JavaScript/Node-specific hook runtime from the source project was intentionally not copied,
  because this repository is Python-first and does not include the source hook dependency chain.
- Rules were rewritten for `pytest`, `pytest-bdd`, and Playwright page-object workflows.
- CI/CD integration is maintained in `.github/workflows/agentic-qa.yml` and `Jenkinsfile`.
