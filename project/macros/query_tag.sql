{% macro build_query_tag(functionality) %}
  {#
    Build a Snowflake query tag string that can be used for:
      - observability (e.g. tracing queries in logs / APM)
      - cost allocation and usage analysis
      - debugging which part of the dbt project issued a query

    Environment resolution:
      - If `var('query_tag_env')` is set, use that value directly.
      - Else, if the database name contains 'DEV' and schema starts with 'dbt_', use 'local_dev'.
      - Else, if the database name contains 'DEV', use 'dev'.
      - Else, if the database name contains 'PROD', use 'prod'.
      - Else, fall back to `target.name`.

    The `functionality` argument should describe what is being executed,
    for example: 'model.my_table', 'seed.my_seed', 'test.unique_orders', etc.
  #}
  {% set db = (target.database or '') | upper %}
  {% set schema = (target.schema or '') %}
  {% set env_override = var('query_tag_env', none) %}

  {% if env_override %}
    {% set env = env_override %}
  {% elif 'DEV' in db and schema.startswith('dbt_') %}
    {% set env = 'local_dev' %}
  {% elif 'DEV' in db %}
    {% set env = 'dev' %}
  {% elif 'PROD' in db %}
    {% set env = 'prod' %}
  {% else %}
    {% set env = target.name %}
  {% endif %}

  {{ return('functionality:' ~ (functionality or 'default') ~ '|env:' ~ env) }}
{% endmacro %}

{% macro set_query_tag(functionality=none) %}
  {#
    Set the Snowflake `query_tag` for the current session.

    Usage patterns:
      - Global pre-hook (recommended):
          models:
            +pre-hook:
              - "{{ set_query_tag('model.' ~ this.name) }}"

      - Ad-hoc / custom usage:
          {{ set_query_tag('seed.my_seed') }}

      - You can also drive functionality via a variable:
          {{ set_query_tag(var('query_tag', 'default')) }}
  #}
  {% if functionality is none %}
    {% set functionality = var('query_tag', 'default') %}
  {% endif %}

  {% set tag = build_query_tag(functionality) %}
  {% do run_query("alter session set query_tag = '" ~ tag ~ "'") %}
{% endmacro %}

