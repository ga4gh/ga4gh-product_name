---
title: "Compliance and conformance testing"
product: "{{PRODUCT_NAME}}"
spec_version: "{{SPEC_VERSION}}"
status: "{{STATUS}}"
last_reviewed: "{{YYYY-MM-DD}}"
owners: "{{OWNERS}}"
---

# Compliance and conformance testing

## Conformance levels

| Level | Requirements | Description |
|---|---|---|
| {{e.g. Core}} | {{SRV-001 to SRV-010}} | {{Minimum for interoperability}} |
| {{e.g. Extended}} | {{Core plus SRV-011 to SRV-020}} | {{Optional capabilities}} |

## Test suite

The conformance test suite lives at {{TEST_SUITE_URL}}.

```bash
{{COMMAND_TO_RUN_TESTS}} --target {{BASE_URL}} --level {{LEVEL}}
```

## Interpreting results

{{Explain pass, fail, skip and warning outcomes, and which failures block a compliance claim.}}

## Reporting results

- Publish the full test report alongside your implementation.
- Add or update your entry on the Implementations page.
- Re-run the suite for each new specification version you claim to support.

## Requirement traceability

<!-- TEMPLATE GUIDANCE: Every requirement ID in the Specification should map to at least one test. Untested requirements are a release risk. -->

| Requirement | Test IDs | Notes |
|---|---|---|
| SRV-001 | {{T-001}} |  |
| SRV-002 | {{T-002, T-003}} |  |
