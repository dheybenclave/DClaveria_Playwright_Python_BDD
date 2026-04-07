---
name: agentic-ci-cd
description: Configure and validate agentic QA execution in GitHub Actions and Jenkins.
---

# /agentic-ci-cd

Use this workflow to maintain CI agentic QA pipelines.

## Pipeline Files

- GitHub Actions: `.github/workflows/agentic-qa.yml`
- Jenkins: `Jenkinsfile`

## Sequence

1. Validate bootstrap checks are present:
   - `verify_env.py`
   - `smoke_collect.py`
2. Ensure marker execution is parameterized.
3. Ensure artifact upload/archive is enabled.
4. Run a CI dry-run in PR or manual dispatch.

## Success Criteria

- CI executes init checks before targeted tests
- Artifacts are uploaded even on failure
- Marker-driven execution works for regression slices
