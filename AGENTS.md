# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Project-Specific Rules

### Test Discovery & Execution
- **Auto-import step definitions**: `conftest.py` auto-discovers steps via glob pattern `tests/step_definitions/**/*.py` - no manual imports needed
- **Run `--collect-only` before every commit** to catch discovery issues (required by Definition of Done)
- **Validation sequence**: 1) targeted test (`pytest -m TC#`), 2) `pytest --collect-only`, 3) regression sweep

### Page Object Pattern
- **Locator naming**: Use `txt_`, `btn_`, `lbl_` prefixes (e.g., `txt_username`, `btn_login`)
- **All locators as `@property` methods returning `Locator`** - never inline selectors in steps
- **Thin steps, rich pages**: Steps delegate to page objects; max 3 lines per step definition

### Test Data Management
- **Load test data via `Config.get_test_data()`** from `tests/test_datas/` directory
- **Never hardcode test data** in page objects or step definitions

### Reporting & Artifacts
- **HTML report**: `test-results/reports/report.html` (self-contained)
- **Screenshots**: Auto-saved on failure to `test-results/screenshots/`
- **Videos**: Only saved on failure when `RECORD_VIDEO=true`
- **Allure**: Auto-served via `npx allure serve` when `AUTO_GENERATE_ALLURE=true`

### Environment
- **Copy `.env.example` to `.env`** - never commit real secrets
- **Required**: `BASE_URL` (https://automationexercise.com)
- **Optional**: `HEADLESS`, `RECORD_VIDEO`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`

### Key Commands
```bash
pytest -m TC6                    # Run single test by marker
pytest --collect-only            # Verify test discovery
HEADLESS=false pytest -m TC6     # Debug with visible browser
```

### Security
- **Mask credentials in logs**: `f"{username[:3]}***@{domain}"`
- **Never print full secret values** in test output

### Detailed Framework Guidelines

For full coding standards, page-object rules, and guardrails see:
- [`.claude/rules/`](.claude/rules/) — Claude / project canonical rule set (guardrails, style, security, framework workflow)
- `.kilo/AGENTS.md` — Kilo AI platform-specific coding guidelines and agent commands
