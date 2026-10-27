---
title: "Contributing"
product: "{{PRODUCT_NAME}}"
spec_version: "{{SPEC_VERSION}}"
status: "{{STATUS}}"
last_reviewed: "{{YYYY-MM-DD}}"
owners: "{{OWNERS}}"
---

# Contributing

## Ways to contribute

- Report a defect or ambiguity in the specification
- Propose a new feature or change
- Improve the documentation or examples
- Add your implementation to the Implementations page

## Before you start

Open an issue to discuss any change to normative text or the schema before writing a pull request. Editorial fixes can go straight to a pull request.

## Workflow

1. Fork the repository and create a branch named `{{type}}/{{short-description}}`.
2. Update the specification text and the schema together in the same pull request.
3. Add or update conformance tests for any new or changed requirement.
4. Add an entry under Unreleased in the Changelog.
5. Run the checks below, then open a pull request.

```bash
{{COMMAND_TO_BUILD_DOCS}}
{{COMMAND_TO_LINT_SCHEMA}}
{{COMMAND_TO_RUN_TESTS}}
```

## Writing style

- Use MUST, SHOULD and MAY in capitals only for normative requirements.
- Write one sentence per line to keep diffs readable.
- Use {{US/British}} English spelling.
- Never include real participant data in examples.

## Review and approval

| Change type | Reviews required | Version impact |
|---|---|---|
| Editorial | 1 maintainer | None or PATCH |
| Non-breaking feature | {{2 maintainers}} | MINOR |
| Breaking change | {{Maintainers plus Work Stream approval}} | MAJOR |

## Code of conduct

All contributors are expected to follow the GA4GH Code of Conduct. See `CODE_OF_CONDUCT.md` in the repository root.

## Licence

By contributing you agree that your contributions are licensed under {{LICENSE}}.
