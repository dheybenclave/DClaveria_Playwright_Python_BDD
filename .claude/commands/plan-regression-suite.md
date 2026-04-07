---
name: plan-regression-suite
description: Plan marker-based regression suites with reuse matrix and execution order.
---

# /plan-regression-suite

Use this workflow to create or revise regression strategy.

## Deliverables

1. Regression scope split:
   - smoke
   - critical path
   - full regression
2. Marker/tag plan (`@TC#`, `@e2e`, area tags)
3. Step reuse matrix (`feature -> steps -> page objects`)
4. CI order:
   - collect
   - smoke/critical
   - full regression

## Example Prompt

"Plan a checkout and account regression suite with marker taxonomy, execution order, and step/page reuse map."
