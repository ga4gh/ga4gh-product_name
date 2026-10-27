---
title: "Getting started"
product: "{{PRODUCT_NAME}}"
spec_version: "{{SPEC_VERSION}}"
status: "{{STATUS}}"
last_reviewed: "{{YYYY-MM-DD}}"
owners: "{{OWNERS}}"
---

# Getting started

<!-- TEMPLATE GUIDANCE: Goal: a new reader makes a successful request within about 15 minutes. Test these steps on a clean machine before each release. -->

## Prerequisites

- {{e.g. Docker 24 or later}}
- {{e.g. curl or another HTTP client}}
- {{Access credentials, if the demo server requires them}}

## Run the reference implementation

1. Clone the repository.
2. Start the server.
3. Confirm it is running by calling the service-info endpoint.

```bash
git clone {{REPO_URL}}
cd {{REPO_NAME}}
{{COMMAND_TO_START_SERVER}}
```

## Make your first request

```bash
curl -s {{BASE_URL}}/service-info
curl -s -H "Authorization: Bearer $TOKEN" {{BASE_URL}}/{{RESOURCE_PATH}}
```

A successful response looks like this:

```json
{
  "{{field}}": "{{value}}"
}
```

## Next steps

- Read the Specification for the full set of requirements
- Work through the Examples for common scenarios
- Run the conformance tests against your implementation
