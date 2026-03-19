<div align="center">

# Playwright Python BDD Automation Framework
**Author:** Dheo Claveria • **Domain:** E2E UI/API testing on `automationexercise.com`  
**Stack:** Playwright (sync) · Pytest · pytest-bdd · xdist · pytest-html · dotenv  
</div>

## What It Is
A lean, interview-ready test framework that demonstrates modern UI automation patterns: BDD-style feature specs, thin step definitions, Page Objects for reuse, and data-driven verification. It targets a public demo site but is structured to drop into enterprise CI with minimal changes.

## What It Does
- Drives realistic browser flows (login, product search, cart/checkout).
- Validates UI state against example tables in Gherkin features.
- Supports parallel runs, headless/headed modes, screenshots/videos on failure.
- Produces portable HTML reports plus debug logs.

## Architecture (paths are absolute for quick reference)
- **Features** `[tests/features](/D:/Automation/Playwright/Python/DClaveria_Playwright_Pythin_BDD/tests/features)` – Gherkin files tagged for selection (e.g., `@TC6`, `@TC7`).
- **Steps** `[tests/step_definitions](/D:/Automation/Playwright/Python/DClaveria_Playwright_Pythin_BDD/tests/step_definitions)` – Declarative glue; delegates to page objects.
- **Page Objects** `[src/pages](/D:/Automation/Playwright/Python/DClaveria_Playwright_Pythin_BDD/src/pages)` – Encapsulate locators and actions (checkout, products, login, signup).
- **Config & utils** `[utils](/D:/Automation/Playwright/Python/DClaveria_Playwright_Pythin_BDD/utils)` – env handling, logging, shared state cleanup.
- **Results** `[test-results](/D:/Automation/Playwright/Python/DClaveria_Playwright_Pythin_BDD/test-results)` – HTML reports, screenshots/videos on failure.
- **Runner settings** `[pytest.ini](/D:/Automation/Playwright/Python/DClaveria_Playwright_Pythin_BDD/pytest.ini)` – marks, logging, html report location.

## Key Design Choices (talking points)
- **Thin steps, rich pages:** Steps stay declarative; page objects own logic and assertions.
- **Data-driven BDD:** Tables in features flow directly into verifications; header normalization is handled in steps.
- **Resilience:** Centralized timeouts and ad blocking in `conftest.py`; cart scraping filters out non-product rows.
- **Observability:** Self-contained HTML reporting, optional videos/screenshots, DEBUG log file for traceability.

## Setup
1) Python 3.8+ installed.  
2) Clone: `git clone https://github.com/BlissCoders/playwright_fundamentals.git`  
3) Create venv & activate:  
   - Windows: `python -m venv .venv && .\\.venv\\Scripts\\activate`  
   - macOS/Linux: `python -m venv .venv && source .venv/bin/activate`
4) Install deps: `pip install -r requirements.txt`
5) Install browsers (first run): `python -m playwright install --with-deps`
6) Optional `.env` overrides (defaults shown):  
   - `BASE_URL=https://automationexercise.com`  
   - `HEADLESS=true`  
   - `RECORD_VIDEO=false`  
   - Credentials: `ADMIN_EMAIL`, `ADMIN_PASSWORD` or `LIST_OF_CREDENTIALS` JSON.

## Running Tests
- Full suite: `pytest`
- Tagged flows (checkout demos): `pytest -m "TC6 or TC7"`
- Parallel: `pytest -n auto`
- Headed debug: `HEADLESS=false pytest -m TC6`
- Collect only: `pytest --collect-only`

## Reporting & Artifacts
- HTML: `test-results/reports/report.html` (per run, self-contained).
- Screenshots: `test-results/screenshots/` on failure.
- Videos: `test-results/videos/` when `RECORD_VIDEO=true`.
- Logs: CLI at INFO; file `test-results/pytest-logs.log` at DEBUG.

## Conventions
- Tags: `@TC#` for traceability, `@e2e`, `@positive_testing` for grouping.
- Scenario names are unique to avoid pytest-bdd collisions.
- Page objects keep assertions close to actions to surface intent and failures quickly.

## Common Interview Highlights
- How BDD maps to code: feature table → step → page object → assertion.
- Stability tactics: centralized timeouts, ad blocking, table-row filtering.
- Scalability: xdist parallelization, environment-driven config, headless/headed toggles.
- Observability: portable HTML reports, artifacts gated by failure to save space.

## Troubleshooting
- Missing browsers: rerun `python -m playwright install --with-deps`.
- Slow external site: raise default timeout in `conftest.py` or set `PLAYWRIGHT_DEFAULT_TIMEOUT`.
- Tag not running: ensure scenario has the tag and name is unique; use `pytest -m "<tag>" --collect-only` to confirm.

## Quick Single-Scenario Run
```bash
pytest -m "TC7"
```
