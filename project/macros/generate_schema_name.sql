{% macro generate_schema_name(custom_schema_name, node) %}
  {# 
    Production:
      - Use folder-level +schema (custom_schema_name) when defined
      - Otherwise fall back to target.schema (e.g. dbt_analytics)
    Non-prod (dev, ci, etc.):
      - Always use target.schema from the profile (e.g. dbt_joachimhodana),
        so everything builds into your personal dataset.
  #}
  {% if target.name in ['prod', 'dev', 'qa', 'ci'] %}
    {{ custom_schema_name or target.schema }}
  {% else %}
    {{ target.schema }}
  {% endif %}
{% endmacro %}
