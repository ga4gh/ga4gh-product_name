:product: {{PRODUCT_NAME}}
:spec-version: {{SPEC_VERSION}}
:status: {{STATUS}}
:last-reviewed: {{YYYY-MM-DD}}
:owners: {{OWNERS}}

============
Service info
============

Implementations of {{PRODUCT_NAME}} MUST implement the `GA4GH Service Info <https://github.com/ga4gh-discovery/ga4gh-service-info>`__ specification at ``/service-info``.

Service type
------------

.. list-table::
   :header-rows: 1

   * - Field
     - Value
   * - ``type.group``
     - ``org.ga4gh``
   * - ``type.artifact``
     - ``{{PRODUCT_SHORT_NAME}}``
   * - ``type.version``
     - The specification version implemented, e.g. ``{{SPEC_VERSION}}``

Example response
----------------

.. code-block:: json

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

Product-specific fields
-----------------------

{{List any additional fields this product adds to the service-info response, or state that there are none.}}

Service registry
----------------

Deployments MAY register with a GA4GH Service Registry to make themselves discoverable.
