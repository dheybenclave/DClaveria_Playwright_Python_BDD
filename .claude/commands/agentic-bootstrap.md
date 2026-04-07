---
name: agentic-bootstrap
description: Bootstrap local agentic QA environment and validate readiness.
---

# /agentic-bootstrap

Use this workflow to initialize local QA automation setup in one pass.

## Steps

1. Run bootstrap:
   - `./scripts/bootstrap_agentic_qa.ps1`
2. Confirm verification output:
   - env PASS
   - dependency PASS
   - collect PASS
3. Run targeted marker:
   - `pytest -m "TC6 or TC7" -q`

## Expected Result

- Local environment is test-ready
- Browser runtime is installed
- Collection and targeted execution are healthy
