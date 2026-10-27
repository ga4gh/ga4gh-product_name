:product: {{PRODUCT_NAME}}
:spec-version: {{SPEC_VERSION}}
:status: {{STATUS}}
:last-reviewed: {{YYYY-MM-DD}}
:owners: {{OWNERS}}

==============================
{{PRODUCT_NAME}} documentation
==============================

..
   TEMPLATE GUIDANCE: Keep this page short. It orients readers and routes them to the right page; detail lives elsewhere.

{{PRODUCT_NAME}} ({{PRODUCT_SHORT_NAME}}) is a GA4GH standard for {{ONE_LINE_PURPOSE}}. This site contains the normative specification, guidance for implementers and the governance record for the product.

At a glance
-----------

.. list-table::
   :header-rows: 1

   * - Item
     - Value
   * - Current version
     - {{SPEC_VERSION}}
   * - Status
     - {{STATUS}}
   * - Work Stream
     - {{WORK_STREAM}}
   * - Repository
     - {{REPO_URL}}
   * - Licence
     - {{LICENSE}}
   * - Contact
     - {{CONTACT_EMAIL}}

Where to start
--------------

.. list-table::
   :header-rows: 1

   * - If you are...
     - Start with
   * - Evaluating whether the standard fits your use case
     - Overview
   * - Building a server or client
     - Getting started, then Specification
   * - Deploying or operating a service
     - Implementer's guide and Security
   * - Proposing a change
     - Contributing

Contents
--------

.. toctree::
   :maxdepth: 2

   Overview <overview>
   Getting started <getting-started>
   Specification <specification/index>
   Data model <specification/data-model>
   API reference <specification/api-reference>
   Security <specification/security>
   Implementer's guide <implementation/implementers-guide>
   Implementations <implementation/implementations>
   Examples <implementation/examples>
   Compliance and conformance testing <conformance/compliance>
   Service info <conformance/service-info>
   Versioning and deprecation <governance/versioning>
   Changelog <governance/changelog>
   Product approval record <governance/product-approval>
   Decision record template <governance/decision-records/adr-template>
   Contributing <contributing>
   Glossary <glossary>
