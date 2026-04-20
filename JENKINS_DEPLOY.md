# Jenkins Deployment Guide — Playwright Python BDD Framework

This guide provides step-by-step instructions to deploy the test automation framework in Jenkins, matching the behavior of GitHub Actions workflows.

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Jenkins Server Setup](#2-jenkins-server-setup)
3. [Plugin Installation](#3-plugin-installation)
4. [Credentials Configuration](#4-credentials-configuration)
5. [Agent/Node Configuration](#5-agentnode-configuration)
6. [Pipeline Job Creation](#6-pipeline-job-creation)
7. [Environment Variables](#7-environment-variables)
8. [Running the Pipeline](#8-running-the-pipeline)
9. [Monitoring & Reports](#9-monitoring--reports)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Prerequisites

### System Requirements

- **Jenkins**: 2.462+ (LTS recommended)
- **Agent OS**: Linux (Ubuntu 22.04+ or Debian) recommended for Playwright browser compatibility
- **Python**: 3.8–3.12
- **Node.js**: 20+ (for Allure report generation; optional)
- **Disk Space**: Minimum 10 GB free (browsers + test artifacts)

### Software Packages (Linux agents)

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv nodejs npm curl wget unzip xvfb libgtk-3-0 libnss3 libasound2 libxss1 libatk-bridge2.0-0 libdrm2 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libatspi2.0-0

# Alternatively, use Playwright's built-in dependency installer
python3 -m playwright install --with-deps
```

---

## 2. Jenkins Server Setup

### 2.1 Install Jenkins

Refer to the official Jenkins installation guide: https://www.jenkins.io/download/

For Ubuntu:
```bash
wget -q -O - https://pkg.jenkins.io/debian/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt-get update
sudo apt-get install jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### 2.2 Initial Jenkins Configuration

1. Unlock Jenkins: `sudo cat /var/lib/jenkins/secrets/initialAdminPassword`
2. Install suggested plugins
3. Create admin user (or use the default admin)
4. Set Jenkins URL (Manage Jenkins → System)

---

## 3. Plugin Installation

Install the following plugins via **Manage Jenkins → Plugins → Available plugins**:

| Plugin | Purpose | Version (minimum) |
|--------|---------|-------------------|
| Pipeline | Jenkins pipeline support | 2.6+ |
| Git | SCM checkout | 4.11+ |
| HTML Publisher | Publish HTML reports | 1.30+ |
| JUnit | Publish test results | 1.48+ |
| NodeJS | Node.js tool installation (optional) | 1.6+ |
| Credentials Binding | Secure credential handling | 1.27+ |
| Workspace Cleanup | Clean old artifacts | 0.45+ |
| Blue Ocean | Modern UI (optional) | 1.27+ |

After installing, restart Jenkins.

---

## 4. Credentials Configuration

Store test credentials securely in Jenkins:

### 4.1 Add Test Credentials (JSON)

If your tests use `LIST_OF_CREDENTIALS` for data-driven scenarios:

1. **Manage Jenkins → Credentials → System → Global credentials (unrestricted) → Add Credentials**
2. Kind: **Secret file** or **Secret text**
   - **Secret file**: Upload a JSON file with credentials
   - **Secret text**: Paste JSON string directly
3. ID: `test-credentials-json` (or any ID you prefer)
4. Description: "Test credentials JSON for BDD scenarios"
5. Secret: `[{"email":"user1@test.com","password":"pass1"},{"email":"user2@test.com","password":"pass2"}]`

**Note**: In the Jenkinsfile, uncomment the line:
```groovy
LIST_OF_CREDENTIALS = credentials('test-credentials-json')
```

### 4.2 Admin Credentials (Optional)

If tests require admin login:

| Credential ID | Type | Secret |
|---------------|------|--------|
| `admin-email` | Secret text | admin@test.com |
| `admin-password` | Secret text | admin123 |

### 4.3 GitHub Personal Access Token (Optional)

For features that interact with GitHub APIs (e.g., reporting), configure:

| Credential ID | Type | Scope |
|---------------|------|--------|
| `github-token` | Secret text | `repo:status`, `read:org` |

---

## 5. Agent/Node Configuration

### 5.1 Create a Linux Build Agent (Recommended)

Playwright browsers work best on Linux with system dependencies installed.

**Option A: Permanent Agent (SSH)**

1. **Manage Jenkins → Manage Nodes and Clouds → New Node**
2. Node name: `playwright-linux`
3. Remote root directory: `/home/jenkins`
4. Launch method: **Launch agent via SSH**
   - Host: `<agent-ip>`
   - Credentials: SSH key pair
   - Java path: `/usr/lib/jvm/java-21-openjdk-amd64/bin/java`

On the agent machine:
```bash
# Install Jenkins agent as service
sudo useradd -m -s /bin/bash jenkins
sudo mkdir -p /home/jenkins
sudo chown jenkins:jenkins /home/jenkins

# Install Java
sudo apt-get install openjdk-21-jdk

# Install Python
sudo apt-get install python3 python3-pip python3-venv

# Install Node.js (optional)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs npm

# Clone agent.jar from Jenkins server (~/agent.jar) and run:
java -jar agent.jar -jnlpUrl <JENKINS_URL>/computer/playwright-linux/slave-agent.jnlp -secret <SECRET>
```

**Option B: Docker Agent (Recommended for isolation)**

Use Jenkins Docker plugin to spin up disposable agents with all dependencies pre-installed.

Example `Dockerfile` for agent:
```dockerfile
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    nodejs npm curl wget unzip \
    xvfb libgtk-3-0 libnss3 libasound2 libxss1 \
    libatk-bridge2.0-0 libdrm2 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libcairo2 libatspi2.0-0 \
    openjdk-21-jdk \
 && rm -rf /var/lib/apt/lists/*

# Install Playwright browsers at build time
RUN python3 -m pip install --upgrade pip && \
    pip install playwright pytest pytest-bdd pytest-html allure-pytest python-dotenv && \
    python3 -m playwright install --with-deps chromium firefox webkit

WORKDIR /workspace
```

Configure Jenkins to use this Docker image as an agent label: `playwright-agent`

### 5.2 Label the Agent

Label the agent with `playwright` to match the pipeline `agent any` or specify `agent { label 'playwright' }`.

---

## 6. Pipeline Job Creation

### 6.1 Create New Pipeline Job

1. **Jenkins Dashboard → New Item**
2. Name: `playwright-bdd-automation`
3. Type: **Pipeline**
4. Click OK

### 6.2 Pipeline Configuration

**General Tab:**
- Check "This project is parameterized"
- Add parameters (as defined in Jenkinsfile):
  - **Boolean Parameter**: `RUN_TARGETED` (default: true)
  - **Boolean Parameter**: `RUN_REGRESSION` (default: false)
  - **Boolean Parameter**: `HEADLESS` (default: true)
  - **Boolean Parameter**: `RECORD_VIDEO` (default: false)
  - **Boolean Parameter**: `PARALLEL` (default: true)
  - **String Parameter**: `PYTEST_MARKER` (default: `TC6 or TC7`)
  - **String Parameter**: `EXTRA_PYTEST_ARGS` (default: empty)

**Pipeline Tab:**
- Definition: **Pipeline script from SCM**
- SCM: **Git**
- Repository URL: `https://github.com/dheybenclave/DClaveria_Playwright_Python_BDD.git`
- Branch: `*/master` (or your target branch)
- Script Path: `Jenkinsfile`
- Additional Behaviors → Check out to a sub-directory (optional): `source`

**Build Triggers:**
- [x] GitHub hook trigger for GITScm polling (if using GitHub integration)
- [x] Poll SCM (if not using webhooks): `H/5 * * * *` (every 5 minutes)
- [x] Build periodically (for scheduled runs): `H 2 * * *` (daily at 2 AM)
- Or trigger manually via **Build with Parameters**

**Advanced Project Options:**
- [x] Do not allow concurrent builds (or as needed)
- Build discards: Keep max 20 builds

**Save** the job.

---

## 7. Environment Variables

The Jenkinsfile sets these environment variables. Optionally override in Jenkins config:

| Variable | Default | Source | Purpose |
|----------|---------|--------|---------|
| `BASE_URL` | `https://automationexercise.com` | Jenkinsfile `environment` block | Target site |
| `PLAYWRIGHT_DEFAULT_TIMEOUT` | `15000` | Jenkinsfile | Timeout in ms |
| `AUTO_GENERATE_ALLURE` | `false` | Jenkinsfile | Auto-generate HTML reports |
| `HEADLESS` | Parameter (`true`) | Build parameter | Run headless |
| `RECORD_VIDEO` | Parameter (`false`) | Build parameter | Capture videos |
| `LIST_OF_CREDENTIALS` | — | Jenkins credentials (optional) | JSON test data |

**Optional: Configure via Jenkins Global Properties**

If you prefer global env vars (Manage Jenkins → Configure System → Global properties):
```
BASE_URL=https://automationexercise.com
PLAYWRIGHT_DEFAULT_TIMEOUT=15000
```

---

## 8. Running the Pipeline

### 8.1 Manual Run with Parameters

1. Open job: `playwright-bdd-automation`
2. Click **Build with Parameters**
3. Configure:
   - `PYTEST_MARKER`: e.g., `TC6`, `TC6 or TC7`, `ui`, `api`, `regression`
   - `RUN_TARGETED`: true (run the marker-based tests)
   - `RUN_REGRESSION`: false (skip full regression unless needed)
   - `HEADLESS`: true
   - `RECORD_VIDEO`: false (enable for debugging)
   - `PARALLEL`: true (recommended for faster feedback)
   - `EXTRA_PYTEST_ARGS`: (optional) e.g., `--tb=short -vv`
4. Click **Build**

### 8.2 Scheduled Run

Configure **Build Triggers → Build periodically**:
```
# Daily at 2 AM
H 2 * * *

# Every 5 minutes (for rapid feedback; use cautiously)
H/5 * * * *
```

### 8.3 Webhook from GitHub

To trigger Jenkins on push/PR:

1. In GitHub repo: Settings → Webhooks → Add webhook
2. Payload URL: `http://<jenkins-server>/github-webhook/`
3. Content type: `application/json`
4. Secret: (optional) configure matching secret in Jenkins GitHub plugin
5. Events: Push, Pull request

In Jenkins:
- Install **GitHub plugin**
- In job config: **Build Triggers → GitHub hook trigger for GITScm polling**

---

## 9. Monitoring & Reports

### 9.1 Jenkins Console Output

View real-time logs: **Build # → Console Output**

Look for:
- `[PASS]`/`[FAIL]` from `verify_env.py`
- `pytest collection succeeded`
- Test execution progress (`44 tests collected`)

### 9.2 Test Reports

After build completes:

| Report | Location in Jenkins | How to Access |
|--------|---------------------|---------------|
| **Pytest HTML** | `test-results/reports/report.html` | Build page → "Pytest HTML Report" link |
| **Allure HTML** | `allure-report/index.html` | Build page → "Allure Report" link (if Node.js available) |
| **JUnit Trends** | Jenkins **Test Result** page | Build page → "Test Result" link |
| **Screenshots** | `test-results/screenshots/` | Artifacts → Browse |
| **Videos** | `test-results/videos/` | Artifacts → Browse (if RECORD_VIDEO=true) |

### 9.3 Artifact Retention

By default, Jenkins keeps artifacts for the build retention policy (configured in **Job → Discard old builds**). Adjust:
- **Max # of builds to keep**: 20
- **Max # of days to keep builds**: 30

The Jenkinsfile's `post` block already archives:
- `test-results/` (HTML reports, screenshots, videos)
- `allure-results/` (raw Allure JSON)
- `allure-report/` (generated HTML)

---

## 10. Troubleshooting

### 10.1 Common Issues

#### Issue: `python3: command not found`

**Cause**: Python not installed on agent or not in PATH.

**Fix**:
```bash
# On agent
sudo apt-get install python3 python3-pip
# Or update PATH in Jenkins node configuration
```

#### Issue: `No module named 'playwright'`

**Cause**: Dependencies not installed.

**Fix**:
- Verify `pip install -r requirements.txt` succeeded
- Check Python version (3.8+ required)
- Ensure virtual environment is not interfering

#### Issue: `pytest --collect-only` fails / no tests collected

**Cause**: Test discovery issues, bad feature file syntax, or missing `__init__.py`.

**Fix**:
1. Check that `tests/` directory has `__init__.py` files
2. Validate `.feature` file syntax (Gherkin)
3. Run locally: `pytest --collect-only -v`
4. Ensure `conftest.py` is present in `tests/`

#### Issue: `playwright install` fails (browser download)

**Cause**: Missing system dependencies or network issues.

**Fix**:
```bash
# On agent, run manually:
python3 -m playwright install --with-deps
# If on headless server without display, ensure xvfb is installed
sudo apt-get install xvfb
```

#### Issue: Allure report not generated

**Cause**: Node.js/npx not installed on agent.

**Fix**:
```bash
# Install Node.js 20+
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
# Verify
npx --version
```
Or disable Allure generation by setting `AUTO_GENERATE_ALLURE=false` and rely on pytest-html.

#### Issue: Tests fail with `TimeoutError` or slow loads

**Cause**: External site (`automationexercise.com`) is slow or unreachable from CI network.

**Fix**:
- Increase timeout in `.env` or Jenkins env: `PLAYWRIGHT_DEFAULT_TIMEOUT=30000`
- Run in non-headless mode temporarily: `HEADLESS=false` to debug
- Check network/firewall restrictions on Jenkins agent

#### Issue: `Permission denied` during shell steps

**Cause**: Agent user lacks execute permissions.

**Fix**:
```bash
# On agent, ensure Jenkins user can run Python/Node
sudo chown -R jenkins:jenkins /workspace
chmod +x .kilo/skills/init/scripts/*.py
```

#### Issue: Missing `LIST_OF_CREDENTIALS`

**Cause**: Jenkins credentials not configured or not referenced.

**Fix**:
1. Add credentials in Jenkins (see Section 4.1)
2. Uncomment in Jenkinsfile:
   ```groovy
   LIST_OF_CREDENTIALS = credentials('test-credentials-json')
   ```
3. Or set in environment: `LIST_OF_CREDENTIALS='[{"email":"test@test.com","password":"pass"}]'`

#### Issue: `publishHTML` fails because report not found

**Cause**: Tests didn't execute or HTML report not generated.

**Fix**: The Jenkinsfile already sets `allowMissing: true`. If still failing, check:
- Did the test stage run? Check `RUN_TARGETED`/`RUN_REGRESSION` params
- Did pytest generate report? Verify `--html=test-results/reports/report.html` is passed

### 10.2 Debugging Steps

1. **Reproduce locally on agent**:
   ```bash
   # SSH into agent
   python3 -m pytest --collect-only
   python3 -m pytest -m TC6 -v --headed
   ```

2. **Check environment**:
   ```bash
   python3 .kilo/skills/init/scripts/verify_env.py
   ```

3. **View Jenkins workspace**:
   - Build → Workspace → Browse files
   - Check if `requirements.txt` is present and correct

4. **Enable verbose logging**:
   - Add `-vv` to `EXTRA_PYTEST_ARGS`
   - Or set `PYTHONIOENCODING=utf-8` in environment

---

## 11. CI/CD Best Practices

### 11.1 Branch-Based Pipelines

Create separate jobs or multibranch pipeline for:
- **`master`** — Full regression nightly, PR validation on every PR
- **`develop`** — Targeted smoke tests on every push
- **`feature/*`** — Run only the scenario being developed (use custom marker)

### 11.2 Parallelism

- Use `PARALLEL=true` for faster feedback (default)
- For flaky networks, consider `PARALLEL=false` to isolate failures

### 11.3 Video & Screenshots

- Enable `RECORD_VIDEO=true` only on failure (`post { always { ... } }` auto-captures)
- Screenshots are automatically taken on test failure via pytest-playwright hooks
- Keep retention low (7–14 days) to save disk space

### 11.4 Notifications

Add to `post` blocks:
```groovy
post {
  failure {
    slackSend channel: '#qa-automation', color: 'danger', message: "Build ${env.BUILD_NUMBER} failed: ${env.JOB_NAME}"
  }
  success {
    slackSend channel: '#qa-automation', color: 'good', message: "Build ${env.BUILD_NUMBER} passed ✅"
  }
}
```

Requires **Slack Notification** plugin and configured credentials.

---

## 12. Security Considerations

- **Never store plaintext credentials** in Jenkinsfile or repo. Use Jenkins Credentials store.
- **Restrict job permissions**: Only authorized users should trigger production runs.
- **Agent isolation**: Use ephemeral agents (Docker/Kubernetes) to prevent cross-contamination.
- **Secrets in reports**: Ensure screenshots/videos don't leak PII. The framework masks credentials in logs by default.

---

## 13. Maintenance

### 13.1 Updating Dependencies

When `requirements.txt` changes:
- Jenkins will auto-install on next run
- Or manually: **Build → Rebuild** (clear cache)

### 13.2 Browser Updates

Playwright browsers auto-update on `playwright install`. To pin versions, set `PLAYWRIGHT_BROWSERS_VERSION` env var.

### 13.3 Cleanup Old Artifacts

Configure **Discard Old Builds**:
- Keep build count: 20
- Keep days: 30
- Artifacts only: 10

Or use `cleanWs()` in `post` block (already in Jenkinsfile).

---

## 14. Quick Reference

| Action | How To |
|--------|--------|
| Trigger manual run | Build with Parameters → Set marker → Build |
| View report | Build number → "Pytest HTML Report" / "Allure Report" |
| Re-run failed tests | Use `EXTRA_PYTEST_ARGS: --lf` (last failed) |
| Debug single test | `EXTRA_PYTEST_ARGS: -k "test_name" -vv --headed` |
| Disable parallel | Set `PARALLEL=false` in parameters |
| Force collection check only | Set `RUN_TARGETED=false`, `RUN_REGRESSION=false`, then manually run `pytest --collect-only` via `sh` step |

---

## 15. Support

For issues or enhancements:
- **Framework issues**: Open GitHub issue in repository
- **Jenkins config**: Contact DevOps/Platform team
- **Playwright docs**: https://playwright.dev/python/docs/intro
- **Pytest-bdd docs**: https://pytest-bdd.readthedocs.io/

---

## Appendix: Jenkinsfile Summary

The included `Jenkinsfile` provides:

- Parameterized builds (marker, parallel, video, headless)
- Environment verification (`.kilo/skills/init/scripts/verify_env.py`)
- Test collection validation (`pytest --collect-only`)
- Targeted test execution (marker-based)
- Full regression suite (optional)
- Allure report generation (if Node.js available)
- HTML report publishing
- Artifact archiving
- Workspace cleanup

See `Jenkinsfile` for full pipeline definition.
