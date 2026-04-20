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
- Step definitions must be thin (1–3 lines) and delegate to page objects.
- All selectors live in page objects under `src/pages/`.

## Failure Triage

When tests fail:
1. Confirm collection still passes.
2. Re-run only failing tag/scenario.
3. Verify selector or timing issue in page object before step edits.
4. Check `test-results/` for screenshots/videos.

## Validation Sequence

When implementing or fixing behavior:
1. Run targeted scenario/tag first (fast feedback).
2. Run `pytest --collect-only` to catch discovery issues.
3. Run broader regression selection before finalizing.

## Done Criteria

- [ ] Scenario(s) for the change pass
- [ ] `pytest --collect-only` passes
- [ ] No new flaky waits or timing hacks
- [ ] Report artifacts remain generated in `test-results/`
