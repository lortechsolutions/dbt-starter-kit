{# 
  Generate schema YAML for an existing model using dbt-codegen.

  Usage (from dbt Cloud / CLI):
    dbt compile --select analysis:codegen.generate_model_yaml

  Then inspect the compiled SQL to copy-paste the generated YAML into
  your `schema.yml` file.
#}

{{ codegen.generate_model_yaml(
    model_name='your_model_name_here',
    upstream_descriptions=true
) }}

