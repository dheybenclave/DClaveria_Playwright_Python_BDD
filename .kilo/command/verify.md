# Verify Environment Command

Verify that the project environment is properly configured for testing.

## Description

This command checks:
1. Python version (>= 3.8)
2. Required Python modules (pytest, playwright, pytest-bdd, dotenv)
3. Environment variables (BASE_URL, HEADLESS)
4. .env file configuration

## Usage

```
kilo "Verify environment setup"
```

or

```
kilo "Run verify command"
```

## Expected Output

```
=== Init Environment Verification ===
[PASS] Python version: 3.x.x (requires >= 3.8)
[PASS/WARN] Virtual environment active
[PASS] Import module: pytest
[PASS] Import module: playwright
[PASS] Import module: pytest_bdd
[PASS] Import module: dotenv
[PASS] .env file found
[PASS] .env key present: BASE_URL=https://...
[PASS] .env key present: HEADLESS=true/false
=== Summary ===
Python: PASS
Dependencies: PASS
Env file: PASS
```

## Troubleshooting

If verification fails:

1. **Python version**: Upgrade Python to >= 3.8
2. **Module import**: Run `pip install -r requirements.txt`
3. **Env file**: Create `.env` with required variables
4. **CI issues**: Ensure GitHub secrets are configured

## Related Commands

- `collect` - Collect test cases
- `test` - Run tests
- `debug` - Debug failing tests
