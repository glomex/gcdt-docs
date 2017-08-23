{{ "Data Structures"|header(2) }}

{% for schema in doc.schemas.get_schemas(['definition'], sort=False) if schema.name != 'top' %}
    {% set schema_header = '{} - structure'.format(schema.name)|header(3) %}
    {% set definition = True %}
    {% set exists_schema = [] %}
    {%- include "schema.rst" -%}
{% endfor -%}
