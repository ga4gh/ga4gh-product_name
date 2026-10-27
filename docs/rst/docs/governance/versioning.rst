:product: {{PRODUCT_NAME}}
:spec-version: {{SPEC_VERSION}}
:status: {{STATUS}}
:last-reviewed: {{YYYY-MM-DD}}
:owners: {{OWNERS}}

==========================
Versioning and deprecation
==========================

Versioning scheme
-----------------

{{PRODUCT_NAME}} uses `Semantic Versioning 2.0.0 <https://semver.org/spec/v2.0.0.html>`__:

- **MAJOR** for changes that break existing compliant implementations
- **MINOR** for backwards-compatible additions
- **PATCH** for clarifications and corrections that do not change required behaviour

What counts as a breaking change
--------------------------------

- Removing or renaming a field, endpoint or parameter
- Making an optional field or parameter required
- Changing the meaning or type of an existing field
- Strengthening a SHOULD to a MUST

Pre-releases
------------

Release candidates use the form ``{{1.2.0-rc.1}}`` and are not covered by the support policy.

Deprecation policy
------------------

#. Mark the element as deprecated in the schema and specification, naming its replacement.
#. Record the deprecation in the Changelog.
#. Keep the element for at least {{N}} months or one MINOR release, whichever is longer.
#. Remove it only in the next MAJOR release.

Supported versions
------------------

.. list-table::
   :header-rows: 1

   * - Version
     - Status
     - Released
     - End of support
   * - {{SPEC_VERSION}}
     - Current
     - {{YYYY-MM-DD}}
     - 
   * - {{PREVIOUS_VERSION}}
     - {{Maintained/Deprecated}}
     - {{YYYY-MM-DD}}
     - {{YYYY-MM-DD}}

Release process
---------------

#. Freeze changes and update the Changelog.
#. Confirm the conformance test suite covers new requirements.
#. Obtain the approvals listed in the Product approval record.
#. Tag the release (``v{{x.y.z}}``) and publish the schema and documentation.
