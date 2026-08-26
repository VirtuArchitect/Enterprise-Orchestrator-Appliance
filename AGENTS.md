# AGENTS.md

## Repository Instructions

This repository contains the Enterprise Orchestrator Appliance: an EAAP-aligned
operator console and local LLM appliance. Treat governance, security, evidence,
approval, execution, audit, packaging, and model-runtime changes as
security-sensitive by default.

## Companion Guides

- For testing strategy, required checks, and smoke testing, follow
  `TESTING_GUIDE.md`.
- For security-sensitive work, follow `SECURITY_REVIEW.md`.
- For code review tasks, follow `CODE_REVIEW.md`.
- Before penetration testing or vulnerability testing, define authorization and
  scope with `PENTEST_SCOPE_TEMPLATE.md`.

## Project Commands

Current foundation-stage commands:

```text
Install: No install step yet.
Lint: Not configured yet.
Format check: Not configured yet.
Type check: Not configured yet.
Unit tests: Not configured yet.
Integration tests: Not configured yet.
End-to-end tests: Not configured yet.
Build: Not configured yet.
Run app: Not configured yet.
Smoke test: python scripts/validate_repository.py
Security scan: GitHub Actions Gitleaks workflow when pushed to GitHub.
```

Update this section as soon as a runtime stack is added.

## Architecture Boundaries

- The LLM is a reasoning component, not the control plane.
- The UI must call governed APIs; it must not call infrastructure tools directly.
- Infrastructure mutation must route through an execution gateway with approval,
  rollback metadata, and audit.
- Prompt packs and model output contracts are versioned product artifacts.
- Air-gapped operation is a design constraint: no runtime dependency on internet
  access, external registries, or floating `latest` images.
- Use pinned versions, checksums, and explicit artifact transfer paths for
  appliance work.

## Project Context

- Read the README, `STATUS.md`, architecture docs, prompt contracts,
  package/build files, test configuration, and nearby code before making edits.
- Prefer existing frameworks, helpers, architecture, naming, and style.
- Keep changes focused on the requested behavior.
- Do not introduce new runtime dependencies unless there is a clear need.
- Do not change public APIs, data schemas, migrations, prompt contracts, model
  runtime boundaries, or security boundaries without calling out the impact.

## Definition of Done

Work is not complete until:

- The requested change is implemented.
- Relevant tests are added or updated, or the reason for not adding tests is
  explained.
- Relevant automated checks are run.
- A smoke test verifies the main changed path.
- Security-sensitive changes receive a security review.
- Remaining risks or skipped checks are documented.

## Required Checks

Use the commands defined by this repository. If commands are unknown, inspect the
project files first, then choose the closest relevant checks.

Recommended check order:

1. Fast targeted test for the changed area.
2. Lint and type checks.
3. Broader test suite when the change has wider risk.
4. Build check when packaging or frontend behavior changed.
5. Manual or automated smoke test.

## Smoke Testing

A smoke test should prove the changed path works at a basic user or system
level.

Examples:

- Start the app and open the changed screen.
- Call the changed API endpoint with a valid request and at least one invalid
  request.
- Run the changed CLI command with a representative input.
- Exercise the changed workflow through the UI.
- Confirm the app starts cleanly after configuration or dependency changes.

Document the exact smoke test in the final response.

## Security Review Trigger

Perform a security review when touching:

- Authentication or sessions.
- Authorization, roles, permissions, or admin features.
- User data, personal data, or sensitive records.
- File upload, download, parsing, previews, or storage.
- SQL, ORM queries, search queries, or database migrations.
- Shell commands, subprocesses, path handling, or filesystem access.
- External webhooks, callbacks, OAuth, tokens, or API keys.
- Logging, analytics, telemetry, or error reporting.
- Dependencies, build, CI/CD, containers, model runtimes, prompts, or deployment
  configuration.

Use `SECURITY_REVIEW.md` for the review checklist.

## Final Response Format

Include:

- Summary of changes.
- Tests and checks run.
- Smoke test performed.
- Security notes if applicable.
- Untested items or residual risk.
