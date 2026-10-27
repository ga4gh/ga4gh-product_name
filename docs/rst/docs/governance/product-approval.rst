:product: {{PRODUCT_NAME}}
:spec-version: {{SPEC_VERSION}}
:status: {{STATUS}}
:last-reviewed: {{YYYY-MM-DD}}
:owners: {{OWNERS}}

=======================
Product approval record
=======================

..
   TEMPLATE GUIDANCE: Check each milestone against the current GA4GH product approval process before relying on this list; this page records what actually happened for this product.

Current status
--------------

.. list-table::
   :header-rows: 1

   * - Item
     - Value
   * - Status
     - {{STATUS}}
   * - Work Stream
     - {{WORK_STREAM}}
   * - Product leads
     - {{OWNERS}}
   * - Approved version
     - {{APPROVED_VERSION}}

Approval history
----------------

.. list-table::
   :header-rows: 1

   * - Date
     - Version
     - Milestone
     - Outcome
     - Record
   * - {{YYYY-MM-DD}}
     - {{x.y.z}}
     - Work Stream approval
     - {{Outcome}}
     - {{Link}}
   * - {{YYYY-MM-DD}}
     - {{x.y.z}}
     - Technical alignment review (TASC)
     - {{Outcome}}
     - {{Link}}
   * - {{YYYY-MM-DD}}
     - {{x.y.z}}
     - Regulatory and ethics review
     - {{Outcome}}
     - {{Link}}
   * - {{YYYY-MM-DD}}
     - {{x.y.z}}
     - Security review
     - {{Outcome}}
     - {{Link}}
   * - {{YYYY-MM-DD}}
     - {{x.y.z}}
     - Public comment period
     - {{Outcome}}
     - {{Link}}
   * - {{YYYY-MM-DD}}
     - {{x.y.z}}
     - Steering Committee approval
     - {{Outcome}}
     - {{Link}}

Driver Projects
---------------

.. list-table::
   :header-rows: 1

   * - Driver Project
     - Role
     - Contact
   * - {{Project}}
     - {{e.g. Champion, early implementer}}
     - {{Name}}

Readiness checklist
-------------------

- [ ] Specification complete, with requirement IDs
- [ ] Machine-readable schema published
- [ ] Reference implementation available
- [ ] Conformance test suite available
- [ ] At least {{N}} independent implementations
- [ ] Security and privacy considerations documented
- [ ] Changelog and versioning policy in place

Review findings
---------------

.. list-table::
   :header-rows: 1

   * - Finding
     - Raised by
     - Resolution
     - Status
   * - {{Finding}}
     - {{Review body}}
     - {{Link to issue or PR}}
     - {{Open/Closed}}
