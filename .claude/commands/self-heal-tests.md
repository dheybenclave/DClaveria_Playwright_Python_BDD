---
name: self-heal-tests
description: Triage and stabilize flaky tests with locator fallback and deterministic waits.
---

# /self-heal-tests

Use this workflow for flaky Playwright tests or unstable selectors.

## Sequence

1. Reproduce failure with smallest marker/scenario.
2. Identify failing locator in page object.
3. Add fallback locator strategy in page object only.
4. Replace timing sleeps with deterministic waits/assertions.
5. Re-run failing marker and related regression tag.

## Guardrails

- Do not move locator logic into step definitions.
- Keep fallback specific to avoid false-positive matches.
- Document root cause and mitigation in PR notes.

## Example Prompt

"Self-heal this flaky selector by adding safe fallback locators and deterministic wait logic in the page object only."
