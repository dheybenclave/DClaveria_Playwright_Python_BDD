# Agentic Migration Notes

## Source and Target

- Source: `D:/Automation/Claude/everything-claude-code`
- Target: `D:/Automation/Playwright/Python/DClaveria_Playwright_Pythin_BDD`

## What Was Migrated

- Python/test-automation focused rule set under `.cursor/rules/`
- Claude command/rule scaffolds under `.claude/`
- Existing project skill `.cursor/skills/init/` retained

## What Was Intentionally Not Migrated

- Source `.cursor/hooks.json` and Node-based hook scripts.
  - Reason: source hooks depend on JavaScript runtime/scripts not present in this repo.
  - Prevents broken hook execution in a Python-first framework.

## Post-Migration Checks

- Validate local environment: `python .cursor/skills/init/scripts/verify_env.py`
- Verify test discovery: `python .cursor/skills/init/scripts/smoke_collect.py`
- Run selected regression tags: `pytest -m "TC6 or TC7"`
