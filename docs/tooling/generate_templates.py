#!/usr/bin/env python3
"""Generate the GA4GH documentation templates in Markdown, reStructuredText and AsciiDoc.

All three formats are rendered from the single content definition in TEMPLATES below,
so edit the content here and re-run rather than editing the generated files by hand:

    python3 tooling/generate_templates.py            # writes markdown/, rst/, asciidoc/
    python3 tooling/generate_templates.py --out DIR  # writes somewhere else

Inline markup in the content uses a small Markdown subset that is converted per format:
`code`, **bold** and [text](url).
"""
import argparse
import re
from pathlib import Path

# --------------------------------------------------------------------------- blocks

def H(level, text): return ("h", level, text)
def P(text): return ("p", text)
def UL(*items): return ("ul", list(items))
def OL(*items): return ("ol", list(items))
def CODE(lang, text): return ("code", lang, text.strip("\n"))
def TABLE(headers, *rows): return ("table", headers, [list(r) for r in rows])
def NOTE(kind, text): return ("note", kind, text)          # note | tip | important | warning
def GUIDE(text): return ("guide", text)                    # author guidance, rendered as a comment
def TOC(*entries): return ("toc", list(entries))           # (path-without-extension, title)

META_FIELDS = [
    ("product", "{{PRODUCT_NAME}}"),
    ("spec-version", "{{SPEC_VERSION}}"),
    ("status", "{{STATUS}}"),
    ("last-reviewed", "{{YYYY-MM-DD}}"),
    ("owners", "{{OWNERS}}"),
]

# --------------------------------------------------------------------------- inline

CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def _protect_code(s, fmt):
    parts = []

    def stash(m):
        parts.append(fmt(m.group(1)))
        return f"\x00{len(parts) - 1}\x00"

    return CODE_RE.sub(stash, s), parts


def _restore(s, parts):
    return re.sub(r"\x00(\d+)\x00", lambda m: parts[int(m.group(1))], s)


def inline_md(s):
    return s


def inline_rst(s):
    s, parts = _protect_code(s, lambda c: f"``{c}``")
    s = LINK_RE.sub(lambda m: f"`{m.group(1)} <{m.group(2)}>`__", s)
    return _restore(s, parts)


def inline_adoc(s):
    s, parts = _protect_code(s, lambda c: f"`+{c}+`")
    s = LINK_RE.sub(lambda m: f"{m.group(2)}[{m.group(1)}]", s)
    return _restore(s, parts)


# --------------------------------------------------------------------------- renderers

def render_md(t):
    out = ["---", f'title: "{t["title"]}"']
    out += [f'{k.replace("-", "_")}: "{v}"' for k, v in META_FIELDS]
    out += ["---", "", f"# {t['title']}", ""]
    for b in t["blocks"]:
        kind = b[0]
        if kind == "h":
            out += ["#" * b[1] + " " + b[2], ""]
        elif kind == "p":
            out += [b[1], ""]
        elif kind == "ul":
            out += [f"- {i}" for i in b[1]] + [""]
        elif kind == "ol":
            out += [f"{n}. {i}" for n, i in enumerate(b[1], 1)] + [""]
        elif kind == "code":
            out += [f"```{b[1]}", b[2], "```", ""]
        elif kind == "table":
            out += ["| " + " | ".join(b[1]) + " |", "|" + "|".join("---" for _ in b[1]) + "|"]
            out += ["| " + " | ".join(r) + " |" for r in b[2]] + [""]
        elif kind == "note":
            out += [f"> **{b[1].capitalize()}:** {b[2]}", ""]
        elif kind == "guide":
            out += [f"<!-- TEMPLATE GUIDANCE: {b[1]} -->", ""]
        elif kind == "toc":
            out += [f"- [{title}]({path}.md)" for path, title in b[1]] + [""]
    return "\n".join(out).rstrip() + "\n"


RST_UNDER = {2: "-", 3: "~"}


def render_rst(t):
    out = [f":{k}: {v}" for k, v in META_FIELDS] + [""]
    title = t["title"]
    out += ["=" * len(title), title, "=" * len(title), ""]
    for b in t["blocks"]:
        kind = b[0]
        if kind == "h":
            out += [b[2], RST_UNDER[b[1]] * len(b[2]), ""]
        elif kind == "p":
            out += [inline_rst(b[1]), ""]
        elif kind == "ul":
            out += [f"- {inline_rst(i)}" for i in b[1]] + [""]
        elif kind == "ol":
            out += [f"#. {inline_rst(i)}" for i in b[1]] + [""]
        elif kind == "code":
            out += [f".. code-block:: {b[1] or 'text'}", ""]
            out += [("   " + line) if line else "" for line in b[2].split("\n")] + [""]
        elif kind == "table":
            out += [".. list-table::", "   :header-rows: 1", ""]
            for row in [b[1]] + b[2]:
                out.append(f"   * - {inline_rst(row[0])}")
                out += [f"     - {inline_rst(c)}" for c in row[1:]]
            out.append("")
        elif kind == "note":
            out += [f".. {b[1]}::", "", "   " + inline_rst(b[2]), ""]
        elif kind == "guide":
            out += ["..", f"   TEMPLATE GUIDANCE: {b[1]}", ""]
        elif kind == "toc":
            out += [".. toctree::", "   :maxdepth: 2", ""]
            out += [f"   {title} <{path}>" for path, title in b[1]] + [""]
    return "\n".join(out).rstrip() + "\n"


def render_adoc(t):
    out = [f"= {t['title']}"] + [f":{k}: {v}" for k, v in META_FIELDS] + [":toc:", ""]
    for b in t["blocks"]:
        kind = b[0]
        if kind == "h":
            out += ["=" * b[1] + " " + b[2], ""]
        elif kind == "p":
            out += [inline_adoc(b[1]), ""]
        elif kind == "ul":
            out += [f"* {inline_adoc(i)}" for i in b[1]] + [""]
        elif kind == "ol":
            out += [f". {inline_adoc(i)}" for i in b[1]] + [""]
        elif kind == "code":
            out += [f"[source,{b[1] or 'text'}]", "----", b[2], "----", ""]
        elif kind == "table":
            out += [f'[cols="{len(b[1])}*",options="header"]', "|==="]
            out += ["|" + " |".join(inline_adoc(c) for c in b[1])]
            out += ["|" + " |".join(inline_adoc(c) for c in r) for r in b[2]]
            out += ["|===", ""]
        elif kind == "note":
            out += [f"{b[1].upper()}: {inline_adoc(b[2])}", ""]
        elif kind == "guide":
            out += ["////", f"TEMPLATE GUIDANCE: {b[1]}", "////", ""]
        elif kind == "toc":
            out += [f"* xref:{path}.adoc[{title}]" for path, title in b[1]] + [""]
    return "\n".join(out).rstrip() + "\n"


FORMATS = {"markdown": ("md", render_md), "rst": ("rst", render_rst), "asciidoc": ("adoc", render_adoc)}

# --------------------------------------------------------------------------- content

PAGES = [
    ("overview", "Overview"),
    ("getting-started", "Getting started"),
    ("specification/index", "Specification"),
    ("specification/data-model", "Data model"),
    ("specification/api-reference", "API reference"),
    ("specification/security", "Security"),
    ("implementation/implementers-guide", "Implementer's guide"),
    ("implementation/implementations", "Implementations"),
    ("implementation/examples", "Examples"),
    ("conformance/compliance", "Compliance and conformance testing"),
    ("conformance/service-info", "Service info"),
    ("governance/versioning", "Versioning and deprecation"),
    ("governance/changelog", "Changelog"),
    ("governance/product-approval", "Product approval record"),
    ("governance/decision-records/adr-template", "Decision record template"),
    ("contributing", "Contributing"),
    ("glossary", "Glossary"),
]

TEMPLATES = [
    {
        "path": "index",
        "title": "{{PRODUCT_NAME}} documentation",
        "blocks": [
            GUIDE("Keep this page short. It orients readers and routes them to the right page; detail lives elsewhere."),
            P("{{PRODUCT_NAME}} ({{PRODUCT_SHORT_NAME}}) is a GA4GH standard for {{ONE_LINE_PURPOSE}}. "
              "This site contains the normative specification, guidance for implementers and the governance record for the product."),
            H(2, "At a glance"),
            TABLE(["Item", "Value"],
                  ["Current version", "{{SPEC_VERSION}}"],
                  ["Status", "{{STATUS}}"],
                  ["Work Stream", "{{WORK_STREAM}}"],
                  ["Repository", "{{REPO_URL}}"],
                  ["Licence", "{{LICENSE}}"],
                  ["Contact", "{{CONTACT_EMAIL}}"]),
            H(2, "Where to start"),
            TABLE(["If you are...", "Start with"],
                  ["Evaluating whether the standard fits your use case", "Overview"],
                  ["Building a server or client", "Getting started, then Specification"],
                  ["Deploying or operating a service", "Implementer's guide and Security"],
                  ["Proposing a change", "Contributing"]),
            H(2, "Contents"),
            TOC(*PAGES),
        ],
    },
    {
        "path": "overview",
        "title": "Overview",
        "blocks": [
            GUIDE("Non-normative. Explain the product in plain language for someone deciding whether it is relevant to them. Avoid MUST/SHOULD here."),
            H(2, "Purpose"),
            P("{{Describe the problem this standard solves, who has that problem, and why a shared standard is better than local solutions.}}"),
            H(2, "Scope"),
            H(3, "In scope"),
            UL("{{Capability or data type covered}}", "{{Capability or data type covered}}"),
            H(3, "Out of scope"),
            UL("{{Explicitly excluded capability, and where it is handled instead if anywhere}}"),
            H(2, "Use cases"),
            GUIDE("Trace each use case to a Driver Project or real deployment where possible."),
            TABLE(["ID", "Use case", "Primary actor", "Driver Project"],
                  ["UC-01", "{{Short description}}", "{{e.g. Researcher, Data steward}}", "{{Project name}}"],
                  ["UC-02", "{{Short description}}", "{{Actor}}", "{{Project name}}"]),
            H(2, "Audiences"),
            UL("**Implementers** building servers, clients or libraries",
               "**Deployers** operating services in production",
               "**Data consumers** querying or retrieving data through compliant services"),
            H(2, "Relationship to other GA4GH standards"),
            TABLE(["Standard", "Relationship"],
                  ["{{e.g. GA4GH Passports}}", "{{e.g. Used to convey a requester's data access permissions}}"],
                  ["Service Info", "Implementations expose a service-info endpoint; see Service info"],
                  ["{{Standard}}", "{{Relationship}}"]),
            H(2, "Maturity"),
            P("This product is currently **{{STATUS}}**. See Versioning and deprecation for the support policy and the Product approval record for its approval history."),
        ],
    },
    {
        "path": "getting-started",
        "title": "Getting started",
        "blocks": [
            GUIDE("Goal: a new reader makes a successful request within about 15 minutes. Test these steps on a clean machine before each release."),
            H(2, "Prerequisites"),
            UL("{{e.g. Docker 24 or later}}", "{{e.g. curl or another HTTP client}}", "{{Access credentials, if the demo server requires them}}"),
            H(2, "Run the reference implementation"),
            OL("Clone the repository.", "Start the server.", "Confirm it is running by calling the service-info endpoint."),
            CODE("bash", """
git clone {{REPO_URL}}
cd {{REPO_NAME}}
{{COMMAND_TO_START_SERVER}}
"""),
            H(2, "Make your first request"),
            CODE("bash", """
curl -s {{BASE_URL}}/service-info
curl -s -H "Authorization: Bearer $TOKEN" {{BASE_URL}}/{{RESOURCE_PATH}}
"""),
            P("A successful response looks like this:"),
            CODE("json", """
{
  "{{field}}": "{{value}}"
}
"""),
            H(2, "Next steps"),
            UL("Read the Specification for the full set of requirements",
               "Work through the Examples for common scenarios",
               "Run the conformance tests against your implementation"),
        ],
    },
    {
        "path": "specification/index",
        "title": "{{PRODUCT_NAME}} specification",
        "blocks": [
            NOTE("important", "This document is normative. Non-normative material is marked as such or lives in the Implementer's guide."),
            H(2, "Conventions"),
            P("The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, NOT RECOMMENDED, MAY and OPTIONAL in this document "
              "are to be interpreted as described in [BCP 14](https://www.rfc-editor.org/info/bcp14) (RFC 2119 and RFC 8174) when, and only when, they appear in all capitals."),
            H(2, "Source of truth"),
            GUIDE("Decide which artefact is authoritative and say so explicitly. Most GA4GH APIs treat the OpenAPI or JSON Schema definition as authoritative for structure and this document as authoritative for behaviour."),
            P("The machine-readable definition at `{{SCHEMA_PATH}}` is authoritative for message structure. "
              "This document is authoritative for behaviour. Any disagreement between them is a defect and should be reported as an issue."),
            H(2, "Version information"),
            TABLE(["Item", "Value"],
                  ["Specification version", "{{SPEC_VERSION}}"],
                  ["Schema version", "{{SCHEMA_VERSION}}"],
                  ["Release date", "{{YYYY-MM-DD}}"],
                  ["Previous version", "{{PREVIOUS_VERSION}}"]),
            H(2, "Architecture"),
            GUIDE("Add a diagram showing the actors, services and data flows. Keep the diagram source (e.g. Mermaid, PlantUML, draw.io) in the repository next to the exported image."),
            P("{{Describe the components and how they interact.}}"),
            H(2, "Requirements"),
            GUIDE("Give every requirement a stable ID so conformance tests and issues can reference it. Never reuse a retired ID."),
            H(3, "Server requirements"),
            UL("**SRV-001** A server MUST {{requirement}}.",
               "**SRV-002** A server SHOULD {{requirement}}."),
            H(3, "Client requirements"),
            UL("**CLI-001** A client MUST {{requirement}}."),
            H(2, "Error handling"),
            TABLE(["HTTP status", "Meaning", "When to use"],
                  ["400", "Bad request", "{{Malformed request or invalid parameter}}"],
                  ["401", "Unauthorised", "Missing or invalid credentials"],
                  ["403", "Forbidden", "Valid credentials without access to the resource"],
                  ["404", "Not found", "{{Resource does not exist or is not visible to the caller}}"],
                  ["500", "Internal server error", "Unexpected server failure"]),
            P("Error responses MUST use the following body:"),
            CODE("json", """
{
  "msg": "{{Human-readable description}}",
  "status_code": 404
}
"""),
            H(2, "Extensibility"),
            P("{{Describe how implementations may add fields or endpoints without breaking interoperability, e.g. namespaced extension fields.}}"),
            H(2, "References"),
            H(3, "Normative references"),
            UL("[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) Key words for use in RFCs to indicate requirement levels",
               "{{Other normative reference}}"),
            H(3, "Informative references"),
            UL("{{Informative reference}}"),
        ],
    },
    {
        "path": "specification/data-model",
        "title": "Data model",
        "blocks": [
            GUIDE("One subsection per entity. Field tables should mirror the schema exactly; consider generating them from the schema in CI to prevent drift."),
            H(2, "Overview"),
            P("{{Summarise the main entities and how they relate. Add an entity-relationship diagram here.}}"),
            H(2, "Entities"),
            H(3, "{{EntityName}}"),
            P("{{What this entity represents.}}"),
            TABLE(["Field", "Type", "Required", "Description"],
                  ["`id`", "string", "Yes", "Identifier, unique within the service"],
                  ["`{{field}}`", "{{type}}", "{{Yes/No}}", "{{Description, including units and format}}"],
                  ["`{{field}}`", "{{type}}", "{{Yes/No}}", "{{Description}}"]),
            CODE("json", """
{
  "id": "{{example-id}}",
  "{{field}}": "{{value}}"
}
"""),
            H(2, "Identifiers"),
            UL("{{Format and allowed characters, e.g. URL-safe string}}",
               "{{Uniqueness scope: per service, global, or CURIE-based}}",
               "{{Whether identifiers are stable over time}}"),
            H(2, "Controlled vocabularies"),
            TABLE(["Field", "Allowed values", "Source"],
                  ["`{{field}}`", "{{Enumerated values or ontology branch}}", "{{e.g. Sequence Ontology, HPO, DUO}}"]),
            H(2, "Schema validation"),
            CODE("bash", """
# OpenAPI
npx @redocly/cli lint {{SCHEMA_PATH}}
# JSON Schema
check-jsonschema --schemafile {{SCHEMA_PATH}} {{EXAMPLE_FILE}}
"""),
        ],
    },
    {
        "path": "specification/api-reference",
        "title": "API reference",
        "blocks": [
            GUIDE("Generate the endpoint-by-endpoint reference from the OpenAPI file where possible (e.g. Redoc, Swagger UI, sphinxcontrib-openapi). Use this page for the narrative the generated reference cannot carry."),
            H(2, "Base URL"),
            P("All endpoints are relative to `{{BASE_URL}}/ga4gh/{{PRODUCT_SHORT_NAME}}/v{{MAJOR_VERSION}}`."),
            H(2, "Authentication"),
            P("See Security for supported authentication methods."),
            H(2, "Endpoint summary"),
            TABLE(["Method", "Path", "Description", "Auth required"],
                  ["GET", "`/service-info`", "Describe this service", "No"],
                  ["GET", "`/{{resources}}`", "{{List resources}}", "{{Yes/No}}"],
                  ["GET", "`/{{resources}}/{id}`", "{{Retrieve one resource}}", "{{Yes/No}}"]),
            H(2, "GET /{{resources}}/{id}"),
            P("{{What this endpoint does and any side effects.}}"),
            H(3, "Parameters"),
            TABLE(["Name", "In", "Type", "Required", "Description"],
                  ["`id`", "path", "string", "Yes", "{{Description}}"],
                  ["`{{param}}`", "query", "{{type}}", "No", "{{Description and default}}"]),
            H(3, "Responses"),
            TABLE(["Status", "Body", "Description"],
                  ["200", "`{{EntityName}}`", "Success"],
                  ["404", "Error", "No such resource"]),
            H(3, "Example"),
            CODE("bash", 'curl -s -H "Authorization: Bearer $TOKEN" {{BASE_URL}}/{{resources}}/{{example-id}}'),
            CODE("json", """
{
  "id": "{{example-id}}"
}
"""),
            H(2, "Pagination and limits"),
            UL("{{Pagination mechanism, e.g. page tokens}}", "{{Maximum page size}}", "{{Rate limits and the response returned when exceeded}}"),
        ],
    },
    {
        "path": "specification/security",
        "title": "Security",
        "blocks": [
            GUIDE("Prepare this page before the GA4GH security and regulatory/ethics reviews; reviewers will expect it."),
            H(2, "Threat model summary"),
            TABLE(["Threat", "Impact", "Mitigation"],
                  ["{{e.g. Token replay}}", "{{Impact}}", "{{Mitigation and related requirement ID}}"],
                  ["{{e.g. Re-identification from aggregate responses}}", "{{Impact}}", "{{Mitigation}}"]),
            H(2, "Authentication"),
            UL("Servers MUST support {{e.g. OAuth 2.0 bearer tokens}}.",
               "{{Describe support for GA4GH Passports and AAI, if applicable}}"),
            H(2, "Authorisation"),
            P("{{How access decisions are made, e.g. Passport visas or data use conditions expressed with the Data Use Ontology (DUO).}}"),
            H(2, "Transport security"),
            UL("All endpoints MUST be served over HTTPS using TLS 1.2 or later.", "{{Additional requirements}}"),
            H(2, "Privacy and data protection"),
            UL("{{Data minimisation requirements}}",
               "Logs SHOULD NOT contain personal data or access tokens.",
               "{{Alignment with the GA4GH Framework for Responsible Sharing of Genomic and Health-Related Data}}"),
            H(2, "Reporting vulnerabilities"),
            P("Report suspected vulnerabilities privately to {{SECURITY_CONTACT}}. Do not open public issues for security problems. See `SECURITY.md` in the repository root."),
        ],
    },
    {
        "path": "implementation/implementers-guide",
        "title": "Implementer's guide",
        "blocks": [
            NOTE("note", "This guide is non-normative. Where it conflicts with the Specification, the Specification takes precedence."),
            H(2, "Design rationale"),
            P("{{Explain the key design choices and the alternatives considered, linking to decision records.}}"),
            H(2, "Recommended practices"),
            UL("{{Practice and why it helps interoperability}}", "{{Practice}}"),
            H(2, "Common pitfalls"),
            TABLE(["Pitfall", "Symptom", "Recommendation"],
                  ["{{Pitfall}}", "{{What users see}}", "{{How to avoid it}}"]),
            H(2, "Performance and scaling"),
            P("{{Guidance on caching, large payloads, streaming and horizontal scaling.}}"),
            H(2, "Working with other GA4GH services"),
            P("{{How this product typically combines with others in a deployment, e.g. DRS, WES, TES, Beacon, Passports.}}"),
            H(2, "Frequently asked questions"),
            H(3, "{{Question}}"),
            P("{{Answer}}"),
        ],
    },
    {
        "path": "implementation/implementations",
        "title": "Implementations",
        "blocks": [
            GUIDE("Listing is self-service via pull request. Record the date each entry was last verified so stale entries can be pruned."),
            P("Known implementations of {{PRODUCT_NAME}}. To add yours, open a pull request against this page."),
            TABLE(["Name", "Type", "Language", "Spec version", "Compliance", "Maintainer", "Link"],
                  ["{{Name}}", "{{Server/Client/Library}}", "{{Language}}", "{{x.y.z}}", "{{Level or 'Not tested'}}", "{{Organisation}}", "{{URL}}"]),
            H(2, "Listing criteria"),
            UL("The implementation is publicly available or offered as a service.",
               "It states which specification version it implements.",
               "Compliance claims are backed by published conformance test results."),
        ],
    },
    {
        "path": "implementation/examples",
        "title": "Examples",
        "blocks": [
            NOTE("warning", "Never include real participant data in examples. Use synthetic or openly licensed reference data only."),
            H(2, "{{Scenario 1: title}}"),
            P("{{Context: who is doing what, and why.}}"),
            OL("{{Step}}", "{{Step}}"),
            CODE("bash", 'curl -s {{BASE_URL}}/{{RESOURCE_PATH}}'),
            CODE("json", '{\n  "{{field}}": "{{value}}"\n}'),
            H(2, "{{Scenario 2: title}}"),
            P("{{Context}}"),
            H(2, "Example data"),
            P("Example files live in `{{EXAMPLES_PATH}}` and are licensed under {{DATA_LICENSE}}."),
        ],
    },
    {
        "path": "conformance/compliance",
        "title": "Compliance and conformance testing",
        "blocks": [
            H(2, "Conformance levels"),
            TABLE(["Level", "Requirements", "Description"],
                  ["{{e.g. Core}}", "{{SRV-001 to SRV-010}}", "{{Minimum for interoperability}}"],
                  ["{{e.g. Extended}}", "{{Core plus SRV-011 to SRV-020}}", "{{Optional capabilities}}"]),
            H(2, "Test suite"),
            P("The conformance test suite lives at {{TEST_SUITE_URL}}."),
            CODE("bash", "{{COMMAND_TO_RUN_TESTS}} --target {{BASE_URL}} --level {{LEVEL}}"),
            H(2, "Interpreting results"),
            P("{{Explain pass, fail, skip and warning outcomes, and which failures block a compliance claim.}}"),
            H(2, "Reporting results"),
            UL("Publish the full test report alongside your implementation.",
               "Add or update your entry on the Implementations page.",
               "Re-run the suite for each new specification version you claim to support."),
            H(2, "Requirement traceability"),
            GUIDE("Every requirement ID in the Specification should map to at least one test. Untested requirements are a release risk."),
            TABLE(["Requirement", "Test IDs", "Notes"],
                  ["SRV-001", "{{T-001}}", ""],
                  ["SRV-002", "{{T-002, T-003}}", ""]),
        ],
    },
    {
        "path": "conformance/service-info",
        "title": "Service info",
        "blocks": [
            P("Implementations of {{PRODUCT_NAME}} MUST implement the [GA4GH Service Info](https://github.com/ga4gh-discovery/ga4gh-service-info) specification at `/service-info`."),
            H(2, "Service type"),
            TABLE(["Field", "Value"],
                  ["`type.group`", "`org.ga4gh`"],
                  ["`type.artifact`", "`{{PRODUCT_SHORT_NAME}}`"],
                  ["`type.version`", "The specification version implemented, e.g. `{{SPEC_VERSION}}`"]),
            H(2, "Example response"),
            CODE("json", """
{
  "id": "{{org.example.service-id}}",
  "name": "{{Service name}}",
  "type": {
    "group": "org.ga4gh",
    "artifact": "{{PRODUCT_SHORT_NAME}}",
    "version": "{{SPEC_VERSION}}"
  },
  "organization": {
    "name": "{{Organisation}}",
    "url": "{{https://example.org}}"
  },
  "version": "{{IMPLEMENTATION_VERSION}}",
  "environment": "{{prod}}"
}
"""),
            H(2, "Product-specific fields"),
            P("{{List any additional fields this product adds to the service-info response, or state that there are none.}}"),
            H(2, "Service registry"),
            P("Deployments MAY register with a GA4GH Service Registry to make themselves discoverable."),
        ],
    },
    {
        "path": "governance/versioning",
        "title": "Versioning and deprecation",
        "blocks": [
            H(2, "Versioning scheme"),
            P("{{PRODUCT_NAME}} uses [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html):"),
            UL("**MAJOR** for changes that break existing compliant implementations",
               "**MINOR** for backwards-compatible additions",
               "**PATCH** for clarifications and corrections that do not change required behaviour"),
            H(2, "What counts as a breaking change"),
            UL("Removing or renaming a field, endpoint or parameter",
               "Making an optional field or parameter required",
               "Changing the meaning or type of an existing field",
               "Strengthening a SHOULD to a MUST"),
            H(2, "Pre-releases"),
            P("Release candidates use the form `{{1.2.0-rc.1}}` and are not covered by the support policy."),
            H(2, "Deprecation policy"),
            OL("Mark the element as deprecated in the schema and specification, naming its replacement.",
               "Record the deprecation in the Changelog.",
               "Keep the element for at least {{N}} months or one MINOR release, whichever is longer.",
               "Remove it only in the next MAJOR release."),
            H(2, "Supported versions"),
            TABLE(["Version", "Status", "Released", "End of support"],
                  ["{{SPEC_VERSION}}", "Current", "{{YYYY-MM-DD}}", ""],
                  ["{{PREVIOUS_VERSION}}", "{{Maintained/Deprecated}}", "{{YYYY-MM-DD}}", "{{YYYY-MM-DD}}"]),
            H(2, "Release process"),
            OL("Freeze changes and update the Changelog.",
               "Confirm the conformance test suite covers new requirements.",
               "Obtain the approvals listed in the Product approval record.",
               "Tag the release (`v{{x.y.z}}`) and publish the schema and documentation."),
        ],
    },
    {
        "path": "governance/changelog",
        "title": "Changelog",
        "blocks": [
            P("All notable changes are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses Semantic Versioning."),
            GUIDE("Write entries for readers of the specification, not for maintainers. Link each entry to its issue or pull request and flag breaking changes with BREAKING."),
            H(2, "Unreleased"),
            H(3, "Added"),
            UL("{{New capability}} ({{#PR}})"),
            H(3, "Changed"),
            UL("{{Change}}"),
            H(3, "Deprecated"),
            UL("{{Deprecated element and its replacement}}"),
            H(3, "Removed"),
            UL("{{Removed element}}"),
            H(3, "Fixed"),
            UL("{{Correction}}"),
            H(3, "Security"),
            UL("{{Security-relevant change}}"),
            H(2, "{{SPEC_VERSION}} ({{YYYY-MM-DD}})"),
            H(3, "Changed"),
            UL("**BREAKING:** {{Description of breaking change and migration path}}"),
        ],
    },
    {
        "path": "governance/product-approval",
        "title": "Product approval record",
        "blocks": [
            GUIDE("Check each milestone against the current GA4GH product approval process before relying on this list; this page records what actually happened for this product."),
            H(2, "Current status"),
            TABLE(["Item", "Value"],
                  ["Status", "{{STATUS}}"],
                  ["Work Stream", "{{WORK_STREAM}}"],
                  ["Product leads", "{{OWNERS}}"],
                  ["Approved version", "{{APPROVED_VERSION}}"]),
            H(2, "Approval history"),
            TABLE(["Date", "Version", "Milestone", "Outcome", "Record"],
                  ["{{YYYY-MM-DD}}", "{{x.y.z}}", "Work Stream approval", "{{Outcome}}", "{{Link}}"],
                  ["{{YYYY-MM-DD}}", "{{x.y.z}}", "Technical alignment review (TASC)", "{{Outcome}}", "{{Link}}"],
                  ["{{YYYY-MM-DD}}", "{{x.y.z}}", "Regulatory and ethics review", "{{Outcome}}", "{{Link}}"],
                  ["{{YYYY-MM-DD}}", "{{x.y.z}}", "Security review", "{{Outcome}}", "{{Link}}"],
                  ["{{YYYY-MM-DD}}", "{{x.y.z}}", "Public comment period", "{{Outcome}}", "{{Link}}"],
                  ["{{YYYY-MM-DD}}", "{{x.y.z}}", "Steering Committee approval", "{{Outcome}}", "{{Link}}"]),
            H(2, "Driver Projects"),
            TABLE(["Driver Project", "Role", "Contact"],
                  ["{{Project}}", "{{e.g. Champion, early implementer}}", "{{Name}}"]),
            H(2, "Readiness checklist"),
            UL("[ ] Specification complete, with requirement IDs",
               "[ ] Machine-readable schema published",
               "[ ] Reference implementation available",
               "[ ] Conformance test suite available",
               "[ ] At least {{N}} independent implementations",
               "[ ] Security and privacy considerations documented",
               "[ ] Changelog and versioning policy in place"),
            H(2, "Review findings"),
            TABLE(["Finding", "Raised by", "Resolution", "Status"],
                  ["{{Finding}}", "{{Review body}}", "{{Link to issue or PR}}", "{{Open/Closed}}"]),
        ],
    },
    {
        "path": "governance/decision-records/adr-template",
        "title": "ADR-{{NNNN}}: {{Decision title}}",
        "blocks": [
            GUIDE("Copy this file to adr-NNNN-short-title and fill it in. Records are immutable once accepted: to change a decision, write a new record that supersedes this one."),
            H(2, "Status"),
            P("{{Proposed / Accepted / Rejected / Superseded by ADR-NNNN}}"),
            H(2, "Context"),
            P("{{What problem or question prompted this decision? Include constraints and relevant requirements.}}"),
            H(2, "Decision drivers"),
            UL("{{e.g. Interoperability with existing GA4GH standards}}", "{{e.g. Ease of implementation}}"),
            H(2, "Options considered"),
            H(3, "Option A: {{name}}"),
            UL("Pros: {{...}}", "Cons: {{...}}"),
            H(3, "Option B: {{name}}"),
            UL("Pros: {{...}}", "Cons: {{...}}"),
            H(2, "Decision"),
            P("{{The option chosen and the reasoning.}}"),
            H(2, "Consequences"),
            UL("{{Positive consequence}}", "{{Negative consequence or trade-off}}", "{{Specification sections or schema elements affected}}"),
            H(2, "Approval"),
            TABLE(["Date", "Approved by", "Discussion"],
                  ["{{YYYY-MM-DD}}", "{{Names or group}}", "{{Link to issue, PR or minutes}}"]),
        ],
    },
    {
        "path": "contributing",
        "title": "Contributing",
        "blocks": [
            H(2, "Ways to contribute"),
            UL("Report a defect or ambiguity in the specification",
               "Propose a new feature or change",
               "Improve the documentation or examples",
               "Add your implementation to the Implementations page"),
            H(2, "Before you start"),
            P("Open an issue to discuss any change to normative text or the schema before writing a pull request. Editorial fixes can go straight to a pull request."),
            H(2, "Workflow"),
            OL("Fork the repository and create a branch named `{{type}}/{{short-description}}`.",
               "Update the specification text and the schema together in the same pull request.",
               "Add or update conformance tests for any new or changed requirement.",
               "Add an entry under Unreleased in the Changelog.",
               "Run the checks below, then open a pull request."),
            CODE("bash", "{{COMMAND_TO_BUILD_DOCS}}\n{{COMMAND_TO_LINT_SCHEMA}}\n{{COMMAND_TO_RUN_TESTS}}"),
            H(2, "Writing style"),
            UL("Use MUST, SHOULD and MAY in capitals only for normative requirements.",
               "Write one sentence per line to keep diffs readable.",
               "Use {{US/British}} English spelling.",
               "Never include real participant data in examples."),
            H(2, "Review and approval"),
            TABLE(["Change type", "Reviews required", "Version impact"],
                  ["Editorial", "1 maintainer", "None or PATCH"],
                  ["Non-breaking feature", "{{2 maintainers}}", "MINOR"],
                  ["Breaking change", "{{Maintainers plus Work Stream approval}}", "MAJOR"]),
            H(2, "Code of conduct"),
            P("All contributors are expected to follow the GA4GH Code of Conduct. See `CODE_OF_CONDUCT.md` in the repository root."),
            H(2, "Licence"),
            P("By contributing you agree that your contributions are licensed under {{LICENSE}}."),
        ],
    },
    {
        "path": "glossary",
        "title": "Glossary",
        "blocks": [
            GUIDE("Keep terms alphabetical. Prefer linking to an authoritative definition over writing a new one, and remove GA4GH terms this product does not use."),
            TABLE(["Term", "Definition", "Source"],
                  ["AAI", "Authentication and Authorisation Infrastructure: the GA4GH standard for how services obtain and validate identity and access claims", "GA4GH"],
                  ["Driver Project", "A real-world genomic data initiative that helps develop and pilot GA4GH standards", "GA4GH"],
                  ["DUO", "Data Use Ontology: machine-readable terms describing permitted uses of a dataset", "GA4GH"],
                  ["Passport", "A bundle of signed claims (visas) describing a researcher's identity and data access permissions", "GA4GH"],
                  ["Service Info", "The GA4GH specification for a common endpoint that describes a service", "GA4GH"],
                  ["TASC", "Technical Alignment Sub-Committee: coordinates technical consistency across GA4GH Work Streams", "GA4GH"],
                  ["Work Stream", "A GA4GH group that develops standards in a particular area", "GA4GH"],
                  ["{{Term}}", "{{Definition}}", "{{Source}}"]),
        ],
    },
]

# --------------------------------------------------------------------------- tooling configs

MKDOCS = """site_name: "{{PRODUCT_NAME}} documentation"
repo_url: "{{REPO_URL}}"
docs_dir: docs
theme:
  name: material   # pip install mkdocs-material
markdown_extensions:
  - admonition
  - tables
  - pymdownx.tasklist
nav:
  - Home: index.md
"""

SPHINX_CONF = '''# Sphinx configuration. Install with: pip install sphinx myst-parser
project = "{{PRODUCT_NAME}}"
author = "{{OWNERS}}"
release = "{{SPEC_VERSION}}"

# myst_parser lets Markdown files sit alongside .rst files in the same tree.
extensions = ["myst_parser"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
myst_enable_extensions = ["colon_fence", "deflist", "tasklist"]

exclude_patterns = ["_build"]
html_theme = "alabaster"  # swap for e.g. "furo" or "sphinx_rtd_theme" if installed
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent.parent))
    out_root = Path(ap.parse_args().out)
    for fmt_dir, (ext, render) in FORMATS.items():
        for t in TEMPLATES:
            dest = out_root / fmt_dir / "docs" / f"{t['path']}.{ext}"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(render(t), encoding="utf-8")
    nav = "".join(f'  - "{title}": {path}.md\n' for path, title in PAGES)
    (out_root / "markdown" / "mkdocs.yml").write_text(MKDOCS + nav, encoding="utf-8")
    (out_root / "rst" / "docs" / "conf.py").write_text(SPHINX_CONF, encoding="utf-8")
    print(f"Wrote {len(TEMPLATES)} templates x {len(FORMATS)} formats to {out_root}")


if __name__ == "__main__":
    main()
