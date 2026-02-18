{# 
  Generate schema YAML for an existing model using dbt-codegen.

  Usage (from dbt Cloud / CLI):
    dbt compile --select analysis:codegen.generate_model_yaml

  Then inspect the compiled SQL to copy-paste the generated YAML into
  your `schema.yml` file.
#}

{# 
  NOTE: dbt-codegen introspects the warehouse (columns) to generate YAML.
  To avoid breaking parsing/compilation in CI tools (e.g. SQLFluff dbt templater),
  this macro is only executed when `execute` is true.
#}

{% if execute %}
  {{ codegen.generate_model_yaml(
      model_names=['your_model_name_here'],
      upstream_descriptions=true,
      include_data_types=true
  ) }}
{% endif %}

