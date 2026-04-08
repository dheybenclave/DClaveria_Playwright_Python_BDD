# Test Debugging Command

Debug and analyze failing tests to identify root causes.

## Description

This command:
1. Runs failing tests with verbose output
2. Analyzes failure causes
3. Suggests fixes for selectors, waits, and assertions
4. Provides debugging tips

## Usage

```
kilo "Debug failing test TC6"
```

or

```
kilo "Debug test login_valid_user"
```

## Debugging Steps

### 1. Run with verbose output
```bash
pytest -v -m TC6 tests/
```

### 2. Run with screenshot on failure
```bash
pytest --screenshot on tests/
```

### 3. Run with video
```bash
HEADLESS=false pytest -m TC6 tests/
```

### 4. Run single test
```bash
pytest -k "test_name" -v tests/
```

## Common Issues

### Selector Failures
- Element not found
- Multiple elements found
- Stale element reference

**Solution**: Use page object locators with fallback strategies

### Timeout Issues
- Page load timeout
- Element wait timeout
- Network timeout

**Solution**: Adjust wait times or use proper wait conditions

### Assertion Failures
- Text mismatch
- Element visibility
- Count mismatch

**Solution**: Verify expected values and page state

## Debugging Tips

1. Use `HEADLESS=false` to see browser
2. Add `print()` statements in step definitions
3. Use `--pause-on-failure` if available
4. Check test reports in `test-results/`

## Related Commands

- `verify` - Verify environment
- `collect` - Collect tests
- `test` - Run tests
