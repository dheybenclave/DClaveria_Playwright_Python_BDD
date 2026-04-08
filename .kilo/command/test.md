# Test Execution Command

Run pytest tests with various options and configurations.

## Description

This command executes pytest tests with support for:
- Specific test markers
- Parallel execution
- Video recording
- Custom test filters

## Usage

### Run all tests
```
kilo "Run all tests"
```

### Run specific marker
```
kilo "Run tests with marker TC6"
```

### Run with parallel
```
kilo "Run tests in parallel"
```

## Common Commands

### Basic execution
```bash
pytest tests/
```

### Run specific marker
```bash
pytest -m "TC6 or TC7" tests/
```

### Run with parallel (CI)
```bash
pytest -n auto --dist loadscope tests/
```

### Run with video
```bash
HEADLESS=false pytest -m TC6 tests/
```

### Run with Allure report
```bash
pytest --alluredir=allure-results tests/
npx allure serve allure-results
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `@TC1`, `@TC2`, etc. | Test case markers |
| `@smoke` | Smoke tests |
| `@regression` | Regression tests |
| `@e2e` | End-to-end tests |

## CI/CD Parallel Execution

### Parallel on push (default)
```bash
pytest -n auto --dist loadscope tests/
```

### Sequential on pull request
```bash
pytest --dist loadscope tests/
```

## Reports

Reports are generated in:
- `test-results/` - Pytest HTML reports
- `allure-results/` - Allure raw results
- `allure-report/` - Allure HTML report
- `tests/reports/` - Custom reports

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests timeout | Increase timeout in conftest.py |
| Parallel failures | Use `--dist loadscope` |
| Video not recording | Set `RECORD_VIDEO=true` |

## Related Commands

- `verify` - Verify environment
- `collect` - Collect tests
- `debug` - Debug tests
