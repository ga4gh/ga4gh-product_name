# Sphinx configuration. Install with: pip install sphinx myst-parser
project = "{{PRODUCT_NAME}}"
author = "{{OWNERS}}"
release = "{{SPEC_VERSION}}"

# myst_parser lets Markdown files sit alongside .rst files in the same tree.
extensions = ["myst_parser"]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
myst_enable_extensions = ["colon_fence", "deflist", "tasklist"]

exclude_patterns = ["_build"]
html_theme = "alabaster"  # swap for e.g. "furo" or "sphinx_rtd_theme" if installed
