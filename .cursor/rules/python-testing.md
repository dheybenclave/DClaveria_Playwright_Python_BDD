---
description: "Python pytest and pytest-bdd testing guidance for this Playwright framework."
globs: ["**/*.py", "**/*.pyi"]
alwaysApply: false
---
# Python Testing

## Framework

- Use `pytest` and `pytest-bdd`.
- Keep feature behavior in `.feature` files and execution logic in Python steps/pages.

## Command Baseline

```bash
pytest --collect-only
pytest -m "TC6 or TC7"
pytest -n auto
```

## Authoring Expectations

- Use explicit assertion messages for easier triage.
- Keep fixtures reusable and scenario-focused.
- Prefer marker/tag-driven execution for regression slicing.

## Failure Triage

When tests fail:
1. Confirm collection still passes.
2. Re-run only failing tag/scenario.
3. Verify selector or timing issue in page object before step edits.
