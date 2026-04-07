# Test Automation Guardrails

## Core Principles

- Keep step definitions declarative and lightweight.
- Put UI operations and assertions in page objects.
- Favor deterministic locators and assertions over sleeps.

## Security and Data Safety

- Never hardcode secrets in tests or page objects.
- Use `.env` / environment variables for credentials.
- Do not print sensitive values in logs or command output.

## Validation Before Completion

- Run a targeted test command for touched behavior.
- Run `pytest --collect-only` to ensure suite integrity.
- Confirm no regressions in tags/scenarios directly related to the change.

## Documentation Discipline

- Keep feature files readable and scenario names unique.
- Update docs/rules when workflow conventions change.
