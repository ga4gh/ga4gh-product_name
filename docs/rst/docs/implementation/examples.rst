:product: {{PRODUCT_NAME}}
:spec-version: {{SPEC_VERSION}}
:status: {{STATUS}}
:last-reviewed: {{YYYY-MM-DD}}
:owners: {{OWNERS}}

========
Examples
========

.. warning::

   Never include real participant data in examples. Use synthetic or openly licensed reference data only.

{{Scenario 1: title}}
---------------------

{{Context: who is doing what, and why.}}

#. {{Step}}
#. {{Step}}

.. code-block:: bash

   curl -s {{BASE_URL}}/{{RESOURCE_PATH}}

.. code-block:: json

   {
     "{{field}}": "{{value}}"
   }

{{Scenario 2: title}}
---------------------

{{Context}}

Example data
------------

Example files live in ``{{EXAMPLES_PATH}}`` and are licensed under {{DATA_LICENSE}}.
