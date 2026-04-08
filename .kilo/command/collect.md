# Test Collection Command

Collect and display all available test cases in the project.

## Description

This command:
1. Scans all BDD feature files
2. Lists all scenarios with markers
3. Shows test coverage summary
4. Displays step definitions mapping

## Usage

```
kilo "Collect all test cases"
```

or

```
kilo "Run collect command"
```

## Common Options

### Collect with markers
```bash
pytest --collect-only -q
```

### Collect specific marker
```bash
pytest --collect-only -m "TC6 or TC7"
```

### Collect with verbose output
```bash
pytest --collect-only -v
```

## Expected Output

```
collected 50 items

<Module tests/features/login.feature>
  <Function login_valid_user>
  <Function login_invalid_password>
  ...
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No tests collected | Check feature file syntax |
| Import errors | Verify step definitions |
| Marker errors | Check marker names in conftest.py |

## Related Commands

- `verify` - Verify environment
- `test` - Run tests
- `debug` - Debug tests
