---
name: feature-development
description: Workflow scaffold for Python Playwright BDD feature development.
---

# /feature-development

Use this workflow when implementing or updating test-automation behavior.

## Goal

Add or update behavior with aligned feature, step, and page object layers.

## Common Files

- `tests/features/**/*.feature`
- `tests/step_definitions/**/*.py`
- `src/pages/**/*.py`
- `utils/**/*.py`

## Suggested Sequence

1. Read current scenario behavior and expected outcomes.
2. Update feature text/tables if business behavior changed.
3. Update step definitions with minimal glue logic.
4. Implement locator/action/assertion changes in page objects.
5. Run targeted marker/scenario.
6. Run `pytest --collect-only` before finalizing.

## Typical Commit Signals

- Add feature scenario coverage
- Update step glue and page behavior
- Improve framework stability or selector reliability
