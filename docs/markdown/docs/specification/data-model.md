---
title: "Data model"
product: "{{PRODUCT_NAME}}"
spec_version: "{{SPEC_VERSION}}"
status: "{{STATUS}}"
last_reviewed: "{{YYYY-MM-DD}}"
owners: "{{OWNERS}}"
---

# Data model

<!-- TEMPLATE GUIDANCE: One subsection per entity. Field tables should mirror the schema exactly; consider generating them from the schema in CI to prevent drift. -->

## Overview

{{Summarise the main entities and how they relate. Add an entity-relationship diagram here.}}

## Entities

### {{EntityName}}

{{What this entity represents.}}

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | string | Yes | Identifier, unique within the service |
| `{{field}}` | {{type}} | {{Yes/No}} | {{Description, including units and format}} |
| `{{field}}` | {{type}} | {{Yes/No}} | {{Description}} |

```json
{
  "id": "{{example-id}}",
  "{{field}}": "{{value}}"
}
```

## Identifiers

- {{Format and allowed characters, e.g. URL-safe string}}
- {{Uniqueness scope: per service, global, or CURIE-based}}
- {{Whether identifiers are stable over time}}

## Controlled vocabularies

| Field | Allowed values | Source |
|---|---|---|
| `{{field}}` | {{Enumerated values or ontology branch}} | {{e.g. Sequence Ontology, HPO, DUO}} |

## Schema validation

```bash
# OpenAPI
npx @redocly/cli lint {{SCHEMA_PATH}}
# JSON Schema
check-jsonschema --schemafile {{SCHEMA_PATH}} {{EXAMPLE_FILE}}
```
