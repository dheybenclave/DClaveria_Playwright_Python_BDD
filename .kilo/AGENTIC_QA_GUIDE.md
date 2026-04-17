# Agentic QA Guide (Kilo-style)

Use this guide when running the framework with Kilo CLI project configuration.

## 1) Project Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Install browsers: `python -m playwright install --with-deps`
3. Run bootstrap checks:
   - `python .cursor/skills/init/scripts/verify_env.py`
   - `python .cursor/skills/init/scripts/smoke_collect.py`
4. Optional one-command bootstrap (Windows):
   - `./scripts/bootstrap_agentic_qa.ps1`

## 2) Kilo Configuration

- Kilo config: `.kilo/kilo.json`
- Hook scripts: `.kilo/hooks/`
- Skills: `.kilo/skills/`
- Rules: `.kilo/rules/`

## 3) Kilo Commands

Kilo provides these built-in commands:

| Command | Description |
|---------|-------------|
| `/verify` | Verify environment setup |
| `/collect` | Collect test cases |
| `/test` | Run pytest tests |
| `/debug` | Debug failing tests |

Usage:
```
kilo "Verify environment setup"
kilo "Run tests with marker TC6"
kilo "Debug failing test"
```

## 4) Kilo Agents

Kilo provides specialized agents:

| Agent | Description |
|-------|-------------|
| `test-planner` | Create comprehensive test plans |
| `test-healer` | Fix failing tests and flaky selectors |
| `test-generator` | Generate test cases from requirements |

Usage:
```
kilo "Use test-planner agent for checkout flow"
kilo "Use test-healer to fix selector failures"
kilo "Use test-generator to create login tests"
```

## 5) Kilo Workflow

1. **Initialize session**:
   - `python .cursor/skills/init/scripts/verify_env.py`
2. **Collect tests**:
   - `pytest --collect-only -q`
3. **Run targeted tests**:
   - `pytest -m "TC6 or TC7" -q`
4. **Use Kilo agents for**:
   - Test planning and analysis
   - Self-healing flaky tests
   - Generating new test cases

## 6) Example Kilo Prompts

- "Use `/verify` to check environment readiness"
- "Use `test-generator` to create tests for new sign-up flow"
- "Use `test-healer` to fix failing selectors on login page"
- "Use `test-planner` to plan regression suite for checkout"

## 7) CI/CD

- GitHub Actions workflow: `.github/workflows/main.yml`
- Agentic QA workflow: `.github/workflows/agentic-qa.yml`
- Jenkins pipeline: `Jenkinsfile`

These pipelines execute init checks and targeted marker runs.

## 8) Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests fail | Run verify_env.py first |
| Selector failures | Use `test-healer` agent |
| Environment issues | Check .env file and env variables |

## 9) Key Paths

| Path | Description |
|------|-------------|
| `tests/features` | BDD feature files |
| `tests/step_definitions` | Step implementations |
| `src/pages` | Page object models |
| `test-results` | Test artifacts |

---

## Reference

- **Unified AGENTS.md**: See [AGENTS.md](./AGENTS.md) for all platform guidelines

### Code Style & Rules (All Platforms)

| Platform | Code Style | Testing Rules | Security |
|----------|------------|---------------|----------|
| **Kilo** | [`.kilo/rules/python-coding-style.md`](.kilo/rules/python-coding-style.md) | [`.kilo/rules/common-testing.md`](.kilo/rules/common-testing.md) | [`.kilo/rules/python-security.md`](.kilo/rules/python-security.md) |
| **Claude** | - | [`.claude/rules/test-automation-guardrails.md`](.claude/rules/test-automation-guardrails.md) | - |
| **Cursor** | [`.cursor/rules/python-coding-style.md`](.cursor/rules/python-coding-style.md) | [`.cursor/rules/common-testing.md`](.cursor/rules/common-testing.md) | [`.cursor/rules/python-security.md`](.cursor/rules/python-security.md) |
