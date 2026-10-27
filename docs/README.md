# GA4GH product documentation templates

A starter set of documentation templates for GA4GH technical products, provided in three equivalent formats.
Delete the folders that re not for your chosen format and fill in the placeholders.

## Layout

```
markdown/   docs/*.md   + mkdocs.yml      (MkDocs, GitHub rendering)
rst/        docs/*.rst  + docs/conf.py    (Sphinx / Read the Docs)
asciidoc/   docs/*.adoc                   (Asciidoctor / Antora)
```

Each format contains the same 18 pages: index, overview, getting started, the specification
(index, data model, API reference, security), implementation (implementer's guide, implementations,
examples), conformance (compliance, service info), governance (versioning, changelog, product approval,
decision record template), contributing and glossary.

## Choosing a format

Pick one format per repository rather than mixing formats within a single docs tree.

- **Markdown** renders directly on GitHub and builds with MkDocs (`pip install mkdocs-material && mkdocs serve`).
  The index uses plain links, so if you build Markdown with Sphinx instead, replace the contents list with a MyST `{toctree}` block.
- **reStructuredText** builds with Sphinx (`pip install sphinx myst-parser && sphinx-build docs docs/_build`).
  The supplied `conf.py` also enables MyST, so Markdown pages can be added to an RST tree if needed.
- **AsciiDoc** builds with Asciidoctor (`asciidoctor -R docs -D build 'docs/**/*.adoc'`) or as an Antora component.

## Placeholders and guidance

- Placeholders use `{{DOUBLE_BRACES}}`. Search for `{{` to find everything that needs filling in.
  The most common are `PRODUCT_NAME`, `PRODUCT_SHORT_NAME`, `SPEC_VERSION`, `STATUS`, `OWNERS`, `WORK_STREAM`,
  `REPO_URL`, `BASE_URL`, `SCHEMA_PATH`, `LICENSE`, `CONTACT_EMAIL` and `SECURITY_CONTACT`.
  Lower-case or descriptive placeholders such as `{{Description}}` are free-text prompts.
- `TEMPLATE GUIDANCE` notes are written as comments (`<!-- -->`, `..`, `////`), so they never render in published output.
  Delete them once a page is complete.
- Each page starts with a metadata block (product, spec version, status, last reviewed, owners):
  YAML front matter in Markdown, Sphinx file-wide metadata in RST, and document attributes in AsciiDoc.
- If you enable the MyST substitutions extension, note that it also uses `{{ }}`; fill in placeholders first.
