## Contributing to the dbt starter kit

Thank you for using and contributing to this enterprise-ready dbt starter.

### Project structure and layering

- **dbt project root**: `project/`
- **Layers** (in `project/models/`):
  - `staging/`: source-aligned, lightly transformed models.
  - `intermediate/`: reusable business logic and joins.
  - `marts/`: consumer-facing facts / dimensions / reporting models.
- New models should be placed in the appropriate layer and grouped by domain using subfolders if needed.

### Modeling conventions

- **Contracts**:
  - All production models should use `config.contract.enforced: true`.
  - Schema YAML must define `version: 2`, `models:`, and `columns` with `name`, `description`, and `data_type`.
- **Tests**:
  - Prefer dbt built-in tests for basic checks (`unique`, `not_null`, relationships).
  - Use `dbt_expectations` for richer data quality (distributions, row counts, etc.).
  - Example: see `project/models/staging/stg_example_orders.sql` and `.yml`.
- **Query tagging**:
  - Query tags are set via `set_query_tag` and wired per layer in `project/dbt_project.yml`.
  - Do not override this globally without updating observability/monitoring expectations.

### Local development workflow

1. Create and activate a Python environment (via `uv`, `venv`, or your preferred tool).
2. Install the project:
   - `pip install .`
3. Install dbt packages:
   - `cd project && dbt deps`
4. Configure your `profiles.yml` with Snowflake (or your adapter) credentials.

Before opening a PR:

- Run dbt:
  - `cd project`
  - `dbt build` (or targeted selection)
- Run tests and linters from repo root:
  - `pre-commit run --all-files`
  - This includes:
    - Python: `black`, `ruff`
    - SQL: `sqlfluff`
    - YAML: `yamllint`
    - Secrets: `gitleaks`
    - Metadata: `scripts/validate_models_yaml.py`

### CI expectations

- All PRs are expected to pass:
  - **Lint**: `.github/workflows/lint.yml`
  - **Model metadata validation**: `.github/workflows/validate-model-metadata.yml`
  - **dbt build (Snowflake CI target)**: `.github/workflows/dbt-build.yml`
  - **Secret scanning**: `.github/workflows/gitleaks.yml`

### Adding new models

When adding a new model:

1. Place it in the correct layer (`staging`, `intermediate`, `marts`).
2. Add a `schema.yml` with:
   - `version: 2`
   - model `name` and `description`
   - `config.contract.enforced: true`
   - `columns` with `name`, `description`, `data_type`
3. Add appropriate tests:
   - Built-in tests.
   - `dbt_expectations` where useful.
4. (Optional but recommended) Add a **unit test** YAML under `project/tests/unit/`.
5. Ensure `dbt build` passes locally before pushing.

