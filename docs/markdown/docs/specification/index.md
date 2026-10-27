---
title: "{{PRODUCT_NAME}} specification"
product: "{{PRODUCT_NAME}}"
spec_version: "{{SPEC_VERSION}}"
status: "{{STATUS}}"
last_reviewed: "{{YYYY-MM-DD}}"
owners: "{{OWNERS}}"
---

# {{PRODUCT_NAME}} specification

> **Important:** This document is normative. Non-normative material is marked as such or lives in the Implementer's guide.

## Conventions

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY and OPTIONAL in this document are to be interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14) (RFC 2119 and RFC 8174) when, and only when, they appear in all capitals.

## Source of truth

<!-- TEMPLATE GUIDANCE: Decide which artefact is authoritative and say so explicitly. Most GA4GH APIs treat the OpenAPI or JSON Schema definition as authoritative for structure and this document as authoritative for behaviour. -->

The machine-readable definition at `{{SCHEMA_PATH}}` is authoritative for message structure. This document is authoritative for behaviour. Any disagreement between them is a defect and should be reported as an issue.

## Version information

| Item | Value |
|---|---|
| Specification version | {{SPEC_VERSION}} |
| Schema version | {{SCHEMA_VERSION}} |
| Release date | {{YYYY-MM-DD}} |
| Previous version | {{PREVIOUS_VERSION}} |

## Architecture

<!-- TEMPLATE GUIDANCE: Add a diagram showing the actors, services and data flows. Keep the diagram source (e.g. Mermaid, PlantUML, draw.io) in the repository next to the exported image. -->

{{Describe the components and how they interact.}}

## Requirements

<!-- TEMPLATE GUIDANCE: Give every requirement a stable ID so conformance tests and issues can reference it. Never reuse a retired ID. -->

### Server requirements

- **SRV-001** A server MUST {{requirement}}.
- **SRV-002** A server SHOULD {{requirement}}.

### Client requirements

- **CLI-001** A client MUST {{requirement}}.

## Error handling

| HTTP status | Meaning | When to use |
|---|---|---|
| 400 | Bad request | {{Malformed request or invalid parameter}} |
| 401 | Unauthorised | Missing or invalid credentials |
| 403 | Forbidden | Valid credentials without access to the resource |
| 404 | Not found | {{Resource does not exist or is not visible to the caller}} |
| 500 | Internal server error | Unexpected server failure |

Error responses MUST use the following body:

```json
{
  "msg": "{{Human-readable description}}",
  "status_code": 404
}
```

## Extensibility

{{Describe how implementations may add fields or endpoints without breaking interoperability, e.g. namespaced extension fields.}}

## References

### Normative references

- [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) Key words for use in RFCs to indicate requirement levels
- {{Other normative reference}}

### Informative references

- {{Informative reference}}
