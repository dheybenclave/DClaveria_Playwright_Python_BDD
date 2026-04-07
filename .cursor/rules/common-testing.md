---
description: "Testing requirements for this repository: collection hygiene, BDD stability, and regression readiness."
alwaysApply: true
---
# Testing Requirements

## Required Validation Sequence

When implementing or fixing behavior:
1. Run targeted scenario/tag first (fast feedback).
2. Run `pytest --collect-only` to catch discovery issues.
3. Run broader regression selection before finalizing.

## Test Types Expected

- BDD E2E scenarios under `tests/features`
- Step definitions under `tests/step_definitions`
- Page object driven assertions under `src/pages`

## Stability Rules

- Keep step definitions thin and delegate UI actions/assertions to page objects.
- Avoid brittle selectors in steps; keep selectors inside page objects.
- Prefer deterministic waits and locator assertions over arbitrary sleeps.
- Preserve tag-driven execution (`@TC#`, `@e2e`, and related markers).

## Definition of Done (Testing)

- [ ] Scenario(s) for the change pass
- [ ] `pytest --collect-only` passes
- [ ] No new flaky waits or timing hacks
- [ ] Report artifacts remain generated in `test-results/`
