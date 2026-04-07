---
name: test-debugging
description: Fast triage flow for failing pytest/pytest-bdd Playwright tests.
---

# /test-debugging

Use this workflow for flaky or failing automation scenarios.

## Triage Flow

1. Reproduce with the smallest failing marker/scenario.
2. Confirm collection integrity with `pytest --collect-only`.
3. Identify failure layer:
   - Feature expectation mismatch
   - Step glue mismatch
   - Page locator/action/assertion mismatch
4. Apply fix in the lowest valid layer (prefer page object first).
5. Re-run failing scenario, then related tags.

## Debug Commands

```bash
HEADLESS=false pytest -m TC6 -q
pytest --collect-only -q
pytest -m "TC6 or TC7" -q
```

## Completion Criteria

- Failure reproduced and root cause documented
- Fix validated in targeted and related runs
- No collection regressions
