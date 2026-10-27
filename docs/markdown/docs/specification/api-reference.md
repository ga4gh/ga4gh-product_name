---
title: "API reference"
product: "{{PRODUCT_NAME}}"
spec_version: "{{SPEC_VERSION}}"
status: "{{STATUS}}"
last_reviewed: "{{YYYY-MM-DD}}"
owners: "{{OWNERS}}"
---

# API reference

<!-- TEMPLATE GUIDANCE: Generate the endpoint-by-endpoint reference from the OpenAPI file where possible (e.g. Redoc, Swagger UI, sphinxcontrib-openapi). Use this page for the narrative the generated reference cannot carry. -->

## Base URL

All endpoints are relative to `{{BASE_URL}}/ga4gh/{{PRODUCT_SHORT_NAME}}/v{{MAJOR_VERSION}}`.

## Authentication

See Security for supported authentication methods.

## Endpoint summary

| Method | Path | Description | Auth required |
|---|---|---|---|
| GET | `/service-info` | Describe this service | No |
| GET | `/{{resources}}` | {{List resources}} | {{Yes/No}} |
| GET | `/{{resources}}/{id}` | {{Retrieve one resource}} | {{Yes/No}} |

## GET /{{resources}}/{id}

{{What this endpoint does and any side effects.}}

### Parameters

| Name | In | Type | Required | Description |
|---|---|---|---|---|
| `id` | path | string | Yes | {{Description}} |
| `{{param}}` | query | {{type}} | No | {{Description and default}} |

### Responses

| Status | Body | Description |
|---|---|---|
| 200 | `{{EntityName}}` | Success |
| 404 | Error | No such resource |

### Example

```bash
curl -s -H "Authorization: Bearer $TOKEN" {{BASE_URL}}/{{resources}}/{{example-id}}
```

```json
{
  "id": "{{example-id}}"
}
```

## Pagination and limits

- {{Pagination mechanism, e.g. page tokens}}
- {{Maximum page size}}
- {{Rate limits and the response returned when exceeded}}
