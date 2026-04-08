---
description: "Python coding style for page objects, step definitions, and test utilities."
globs: ["**/*.py", "**/*.pyi"]
alwaysApply: false
---
# Python Coding Style

## Standards

- Follow PEP 8 and keep functions focused.
- Add type hints for new/changed function signatures.
- Prefer descriptive method names reflecting user behavior.

## Framework Structure

- Keep page objects as the source of locator/action truth.
- Keep step definitions declarative and minimal.
- Place shared helpers in `utils/` and avoid duplicate logic.

## Readability

- Use explicit waits/assertions instead of timing sleeps.
- Raise clear assertion failures with expected vs actual context.
