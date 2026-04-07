---
name: generate-test-cases
description: Generate pytest-bdd test cases from requirements using existing framework patterns.
---

# /generate-test-cases

Use this workflow to generate new test coverage quickly and consistently.

## Inputs

- Requirement statement or user story
- Target marker/tag (example: `@TC12`)
- Expected positive and negative behaviors

## Output Targets

- Feature file: `tests/features/**`
- Step glue: `tests/step_definitions/**`
- Page updates (if needed): `src/pages/**`

## Rules

- Keep steps thin; put locator/action/assertion logic in page objects.
- Reuse existing step patterns before adding new step definitions.
- Include scenario outline examples for data-driven cases.

## Example Prompt

"Generate login and lockout test cases for invalid credentials and add feature + steps using existing page object methods."
