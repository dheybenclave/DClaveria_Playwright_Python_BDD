<div align="center">

# Playwright Python BDD Automation Framework

**Author:** Dheyb Claveria  
**Domain:** E2E UI/API testing on `automationexercise.com`  
**Stack:** Playwright (sync) · Pytest · pytest-bdd · pytest-html · allure-pytest · dotenv

</div>

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Architecture](#2-architecture)
3. [Setup](#3-setup)
4. [Running Tests](#4-running-tests)
5. [Test Organization](#5-test-organization)
6. [Environment Variables](#6-environment-variables)
7. [Reporting](#7-reporting)
8. [AI Agent Configuration](#8-ai-agent-configuration)
9. [CI/CD](#9-cicd)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Project Overview

A production-ready test automation framework demonstrating modern UI + API automation patterns:

- **BDD-style Gherkin specs** in `tests/features/`
- **Thin step definitions** that delegate to page objects
- **Rich Page Objects** encapsulating locators, actions, and assertions
- **Data-driven testing** with feature tables
- **Security testing** (XSS, SQL injection, authentication)
- **Accessibility testing** (basic a11y validations)
- **Multi-AI platform support** (Claude, Cursor, Kilo)

---

## 2. Architecture

```
DClaveria_Playwright_Python_BDD/
├── tests/
│   ├── features/              # Gherkin .feature files
│   │   ├── e2e_suites/       # Full user journey flows
│   │   ├── regression_suites/ # Critical path validation (login, sign-up)
│   │   ├── api_suites/       # REST API CRUD operations
│   │   ├── security_suites/  # XSS, SQL injection, auth tests
│   │   └── accessibility_suites/ # WCAG validations
│   ├── step_definitions/      # Thin step glue
│   │   ├── ui/               # login, sign_up, products, checkout, payment, common
│   │   ├── api/              # user, order, search, brands, products
│   │   ├── security/         # authentication, xss, sql_injection
│   │   └── accessibility/    # a11y checks
│   └── test_datas/          # JSON, CSV data files
├── src/
│   └── pages/
│       ├── ui/              # Rich page objects (locators + actions)
│       ├── api/             # API client layer
│       ├── base_page.py     # Core UI base class
│       └── common_page.py   # Shared UI utilities
├── utils/
│   ├── config.py            # Environment & secrets loader
│   ├── logger.py            # Structured logging
│   ├── test_state.py        # Cross-step state sharing
│   ├── api_helpers.py       # HTTP session helpers
│   └── security_payloads.py # Malicious input vectors
├── conftest.py              # Pytest fixtures & hooks
├── pytest.ini               # Pytest config (markers, timeout)
├── requirements.txt         # Python dependencies
├── test-results/            # HTML reports, screenshots, videos
├── allure-results/          # Raw Allure JSON
├── .env                     # Local secrets (git-ignored)
├── .github/workflows/       # CI pipelines
├── scripts/                 # Bootstrap & helper scripts
├── .claude/                 # Claude AI config & agents
├── .cursor/                 # Cursor AI config & agents
└── .kilo/                   # Kilo AI config & agents
```

---

## 3. Setup

### Prerequisites

- Python 3.8+
- Git

### Installation

```powershell
# 1. Clone the repository
git clone https://github.com/dheybenclave/DClaveria_Playwright_Python_BDD.git
cd DClaveria_Playwright_Python_BDD

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install Playwright browsers
python -m playwright install --with-deps
```

### Environment Configuration

Create a `.env` file in the root directory (copy from `.env.example` if provided):

```env
# Required - Target application
BASE_URL=https://automationexercise.com

# Optional - Browser behavior
HEADLESS=true
RECORD_VIDEO=false
PLAYWRIGHT_DEFAULT_TIMEOUT=15000

# Optional - Test accounts (for multi-user scenarios)
ADMIN_EMAIL=admin@test.com
ADMIN_PASSWORD=admin123
LIST_OF_CREDENTIALS='[{"email":"user@test.com","password":"pass123"}]'

# Optional - Reporting
AUTO_GENERATE_ALLURE=false
```

**Security note:** `.env` is git-ignored. Never commit real credentials.

---

## 4. Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run single test by marker (preferred)
pytest -m TC6

# Run by keyword in scenario name
pytest -k "login"

# Run API tests only
pytest -m api

# Run UI tests only
pytest -m ui

# Run regression suite
pytest -m regression
```

### Advanced Options

```bash
# Parallel execution
pytest -n auto

# Headed mode (visible browser for debugging)
HEADLESS=false pytest -m TC6

# Verify test discovery (always run before committing)
pytest --collect-only

# Generate HTML report
pytest --html=test-results/reports/report.html --self-contained-html

# Run with video recording
RECORD_VIDEO=true pytest -m TC6

# Run with Allure reporting
pytest --alluredir=allure-results
```

### Open Allure Reports

```bash
# Generate Allure HTML
npx allure generate allure-results -o allure-report

# Open Allure report
npx allure open allure-report

# Serve Allure results
npx allure serve allure-results
```

---

## 5. Test Organization

### Feature Suites

| Suite | Folder | Description |
|-------|--------|-------------|
| E2E | `tests/features/e2e_suites/` | Full checkout flows |
| Regression | `tests/features/regression_suites/` | Login, sign-up |
| API | `tests/features/api_suites/` | User, Order, Product, Brand, Search CRUD |
| Security | `tests/features/security_suites/` | XSS, SQL injection, authentication |
| Accessibility | `tests/features/accessibility_suites/` | Basic a11y validations |

### Step Definitions

| Type | Location | Examples |
|------|----------|----------|
| UI | `tests/step_definitions/ui/` | login, sign_up, products, checkout, payment |
| API | `tests/step_definitions/api/` | user, order, search, brands, products |
| Security | `tests/step_definitions/security/` | authentication, xss, sql_injection |
| Accessibility | `tests/step_definitions/accessibility/` | a11y |

### Page Objects

| Type | Location | Examples |
|------|----------|----------|
| UI | `src/pages/` | login_page, signup_page, products_page |
| API | `src/pages/api/` | base_api, user, order, search |

---

## 6. Environment Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `BASE_URL` | <https://automationexercise.com> | Yes | Target application URL |
| `HEADLESS` | true | No | Run browser in headless mode |
| `RECORD_VIDEO` | false | No | Record test videos on failure |
| `PLAYWRIGHT_DEFAULT_TIMEOUT` | 15000 | No | Global timeout in milliseconds |
| `ADMIN_EMAIL` | - | No | Admin account email |
| `ADMIN_PASSWORD` | - | No | Admin account password |
| `LIST_OF_CREDENTIALS` | - | No | JSON array of test credentials |
| `AUTO_GENERATE_ALLURE` | false | No | Auto-generate Allure reports |

---

## 7. Reporting

| Artifact | Location | Description |
|----------|----------|-------------|
| HTML Report | `test-results/reports/report.html` | Self-contained HTML report |
| Allure Results | `allure-results/` | Raw Allure results |
| Allure HTML | `allure-report/` | Generated Allure HTML |
| Screenshots | `test-results/screenshots/` | Screenshots on failure |
| Videos | `test-results/videos/` | Test videos when RECORD_VIDEO=true |
| Logs | `test-results/pytest-logs.log` | DEBUG level logs |

---

## 8. AI Agent Configuration

This project uses **three synchronized AI platforms** for agentic QA automation.

### Platform Overview

| Platform | Config File | Rules Directory | Docs |
|----------|-------------|-----------------|------|
| Claude | `.claude/settings.json` | `.claude/rules/` | `CLAUDE.md` |
| Cursor | `.cursor/hooks.json` | `.cursor/rules/` | `CURSOR.md` |
| Kilo | `.kilo/kilo.json` | `.kilo/rules/` | `KILO.md` |

**Unified Guide:** See `AGENTS.md` for all platform guidelines.

### Claude Agents (`.claude/agents/`)

| Agent | Description |
|-------|-------------|
| test-executor | Run smoke, regression, E2E, API, security tests |
| test-architect | Framework design, code review, architecture |
| product-owner | Requirements analysis, user stories |
| scrum-master | Team coordination, sprint planning |

### Kilo Agents (`.kilo/agent/`)

| Agent | Description |
|-------|-------------|
| test-executor | Run tests, analyze results |
| test-architect | Framework architecture |
| product-owner | Requirements analysis |
| scrum-master | Team coordination |
| test-planner | Test planning |
| test-healer | Fix flaky tests |
| test-generator | Generate test cases |

### Session Start Actions

Each platform runs startup hooks to verify environment:

```bash
# Verify environment
python .cursor/skills/init/scripts/verify_env.py

# Collect tests
python .cursor/skills/init/scripts/smoke_collect.py
```

### Sync Strategy

When updating rules:

1. Make change in primary location
2. Copy to all three directories: `.claude/rules/`, `.cursor/rules/`, `.kilo/rules/`
3. Run `pytest --collect-only` to validate

---

## 9. CI/CD

### GitHub Actions

| Workflow | File | Description |
|----------|------|-------------|
| Main | `.github/workflows/main.yml` | Standard test execution on push/PR |
| Agentic QA | `.github/workflows/agentic-qa.yml` | AI-powered validation workflow |

### Jenkins

| Item | Details |
|------|---------|
| Pipeline file | `Jenkinsfile` |
| Deployment guide | `JENKINS_DEPLOY.md` |
| Required plugins | Pipeline, Git, HTML Publisher, JUnit, Credentials Binding |
| Agent OS | Linux (Ubuntu 22.04+ recommended) |
| Key parameters | `PYTEST_MARKER`, `RUN_TARGETED`, `RUN_REGRESSION`, `HEADLESS`, `RECORD_VIDEO`, `PARALLEL` |

**Quick start**: See `JENKINS_DEPLOY.md` for step-by-step setup.

### Local Bootstrap

```powershell
# PowerShell
.\scripts\bootstrap_agentic_qa.ps1
```

---

## 10. Troubleshooting

| Issue | Solution |
|-------|----------|
| Missing browsers | `python -m playwright install --with-deps` |
| Slow external site | Increase `PLAYWRIGHT_DEFAULT_TIMEOUT` in `.env` |
| Tag not found | Run `pytest -m "<tag>" --collect-only` |
| Test discovery fails | Run `pytest --collect-only` to debug |
| Import errors | Ensure venv is activated |
| Credentials not loading | Check `.env` file exists |

---

## Pytest Markers Reference

| Marker | Description |
|--------|-------------|
| `@TC#` | Specific test case ID (e.g., `@TC6`, `@TC7`) |
| `@ui` | UI/E2E tests |
| `@api` | API CRUD tests |
| `@regression` | Full regression suite |
| `@login` | Login page tests |
| `@signup` | Sign-up page tests |
| `@products` | Products page tests |
| `@checkout` | Checkout flow tests |
| `@payment` | Payment tests |
| `@positive_testing` | Happy path scenarios |
| `@negative_testing` | Error/edge case scenarios |
| `@security` | Security-focused tests (XSS, SQLi, auth) |

---

## Documentation Reference

| File | Purpose |
|------|---------|
| `AGENTS.md` | Unified AI agent guidelines (Claude, Cursor, Kilo) |
| `CLAUDE.md` | Claude-specific configuration |
| `CURSOR.md` | Cursor-specific configuration |
| `KILO.md` | Kilo-specific configuration |
| `.kilo/AGENTIC_QA_GUIDE.md` | Claude workflow guide |
| `.kilo/AGENTIC_QA_GUIDE.md` | Cursor workflow guide |
| `.kilo/rules/` | Framework rule set (linting, testing, security) |

---

## Quick Start Summary

```bash
# 1. Setup
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install --with-deps

# 2. Verify
pytest --collect-only

# 3. Run tests
pytest -m TC6

# 4. Debug
HEADLESS=false pytest -m TC6 -v
```

---

**For AI agent commands, see `AGENTS.md`**
