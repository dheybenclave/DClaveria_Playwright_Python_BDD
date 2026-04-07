---
name: init
description: Initialize this Playwright Python BDD project for local test execution by validating Python/venv/dependencies, installing browsers, checking environment variables, and running a smoke collection step. Use when the user asks to initialize, bootstrap, set up, or verify test-run readiness.
---

# Init

## Purpose
Use this skill to bootstrap a reliable local test run for this repository.

## Workflow Checklist
Copy this checklist and track progress:

```markdown
Init Progress:
- [ ] Step 1: Verify Python and virtual environment
- [ ] Step 2: Install or validate dependencies
- [ ] Step 3: Install Playwright browsers
- [ ] Step 4: Validate env configuration
- [ ] Step 5: Run smoke collection
- [ ] Step 6: Report readiness and next command
```

## Step 1: Verify Python and virtual environment
Run:

```bash
python --version
python .cursor/skills/init/scripts/verify_env.py
```

If no virtual environment is active, create and activate one:

```bash
python -m venv .venv
```

Then activate it based on OS:
- Windows (PowerShell): `.venv/Scripts/Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Run `python .cursor/skills/init/scripts/verify_env.py` again after activation.

## Step 2: Install or validate dependencies
Run:

```bash
pip install -r requirements.txt
```

If installation fails, stop and report the exact package failure.

## Step 3: Install Playwright browsers
Run:

```bash
python -m playwright install --with-deps
```

If `--with-deps` is unsupported in the environment, retry with:

```bash
python -m playwright install
```

## Step 4: Validate env configuration
Run:

```bash
python .cursor/skills/init/scripts/verify_env.py
```

Review `.env` values only for presence/shape (never print secrets in full). Required keys:
- `BASE_URL`
- `HEADLESS`

Optional keys:
- `RECORD_VIDEO`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `LIST_OF_CREDENTIALS`

## Step 5: Run smoke collection
Run:

```bash
python .cursor/skills/init/scripts/smoke_collect.py
```

If collection fails, report top error and likely fix.

## Step 6: Report readiness and next command
Use this output format:

```markdown
Init Result:
- Environment: PASS/FAIL
- Dependencies: PASS/FAIL
- Browsers: PASS/FAIL
- Env file: PASS/FAIL
- Pytest collect: PASS/FAIL

Recommended next command:
- `pytest -m "TC6 or TC7"`
```

## Utility Scripts
- Detailed environment checks: [scripts/verify_env.py](scripts/verify_env.py)
- Fast pytest collection smoke test: [scripts/smoke_collect.py](scripts/smoke_collect.py)
