---
description: "Python test automation security guidance: secrets, logs, and safe assertions."
globs: ["**/*.py", "**/*.pyi", "**/.env*", "**/*.feature"]
alwaysApply: false
---
# Python Security

## Secret Management

- Never hardcode credentials, tokens, or API keys.
- Load secrets through environment variables or `.env`.
- Never print full secret values in logs or test output.

## Test Data and Logging

- Use masked output for credentials during debug.
- Do not commit sensitive `.env` values.
- Keep screenshots/videos free of sensitive account details when possible.

## Safe Automation Practices

- Validate external input before using it in assertions or URL construction.
- Avoid executing shell/user-supplied text without sanitization.
