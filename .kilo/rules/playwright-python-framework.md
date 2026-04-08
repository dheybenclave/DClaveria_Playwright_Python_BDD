---
description: "Repository-specific Playwright + pytest-bdd framework conventions and execution workflow."
alwaysApply: true
---
# Playwright Python Framework Conventions

## Key Paths

- Features: `tests/features`
- Steps: `tests/step_definitions`
- Pages: `src/pages`
- Utilities/config: `utils`
- Artifacts: `test-results`

## Workflow

1. Update or add scenario behavior in feature files.
2. Implement step glue with minimal logic.
3. Implement page-level actions/assertions.
4. Run targeted tag/scenario and then collection.

## Command Quickstart

```bash
pytest
pytest -m "TC6 or TC7"
pytest --collect-only
HEADLESS=false pytest -m TC6
```

## Reliability Guardrails

- Do not put selectors directly in step definition files.
- Keep waits centralized and deterministic.
- Preserve existing marker naming and report output paths.
