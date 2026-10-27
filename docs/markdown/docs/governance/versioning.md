---
title: "Versioning and deprecation"
product: "{{PRODUCT_NAME}}"
spec_version: "{{SPEC_VERSION}}"
status: "{{STATUS}}"
last_reviewed: "{{YYYY-MM-DD}}"
owners: "{{OWNERS}}"
---

# Versioning and deprecation

## Versioning scheme

{{PRODUCT_NAME}} uses [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html):

- **MAJOR** for changes that break existing compliant implementations
- **MINOR** for backwards-compatible additions
- **PATCH** for clarifications and corrections that do not change required behaviour

## What counts as a breaking change

- Removing or renaming a field, endpoint or parameter
- Making an optional field or parameter required
- Changing the meaning or type of an existing field
- Strengthening a SHOULD to a MUST

## Pre-releases

Release candidates use the form `{{1.2.0-rc.1}}` and are not covered by the support policy.

## Deprecation policy

1. Mark the element as deprecated in the schema and specification, naming its replacement.
2. Record the deprecation in the Changelog.
3. Keep the element for at least {{N}} months or one MINOR release, whichever is longer.
4. Remove it only in the next MAJOR release.

## Supported versions

| Version | Status | Released | End of support |
|---|---|---|---|
| {{SPEC_VERSION}} | Current | {{YYYY-MM-DD}} |  |
| {{PREVIOUS_VERSION}} | {{Maintained/Deprecated}} | {{YYYY-MM-DD}} | {{YYYY-MM-DD}} |

## Release process

1. Freeze changes and update the Changelog.
2. Confirm the conformance test suite covers new requirements.
3. Obtain the approvals listed in the Product approval record.
4. Tag the release (`v{{x.y.z}}`) and publish the schema and documentation.
