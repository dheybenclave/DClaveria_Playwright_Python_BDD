# AGENTS.md - Debug Mode Rules

This file provides guidance to agents when working with code in this repository.

## Non-Obvious Debug Rules

### Test Discovery Issues
- **Auto-import step definitions**: `conftest.py` auto-discovers steps via glob pattern `tests/step_definitions/**/*.py`
- **If steps aren't found**: Run `pytest --collect-only` to verify discovery
- **Common issue**: Step files named `test_*.py` or `*_test.py` are auto-discovered; others need the glob pattern

### Debugging UI Tests
- **Use `HEADLESS=false`** for visible browser debugging
- **Videos**: Only saved on failure when `RECORD_VIDEO=true`
- **Screenshots**: Auto-saved on failure to `test-results/screenshots/`

### Log Locations
- **Test logs**: `test-results/pytest-logs.log` (DEBUG level)
- **Allure results**: `allure-results/` (raw JSON)
- **HTML report**: `test-results/reports/report.html`

### Common Gotchas
- **Ad blocking**: `conftest.py` blocks googleads, ads-twitter, facebook domains
- **Video cleanup**: Videos deleted on pass; only saved on failure
- **Test state**: Use `utils/test_state.py` for cross-step state sharing