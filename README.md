## dbt starter kit

![Lortechsolutions](./static/images/banner.png)

This repo is an **opinionated, enterprise-ready dbt starter project**, including:

- **Layered modeling structure** (`staging`, `intermediate`, `marts`)
- **Contracts-first models** with example enforced contracts
- **Rich testing** via dbt built-ins and `dbt-expectations`
- **Strong CI** (linting, model metadata validation, dbt build, secrets scanning)
- **Observability hooks** via Snowflake `query_tag` per layer

> **Tooling note:** The starter was created with [`uv`](https://github.com/astral-sh/uv) in mind for dependency and environment management, but it works perfectly fine with a standard Python toolchain as well (e.g. `python -m venv`, `pip install -r requirements.txt`, Poetry, etc.).

### Quick start

1. **Install dependencies** in your Python environment:

   ```bash
   pip install .
   cd project && dbt deps
   ```

2. **Configure dbt profile** (Snowflake by default):
   - Add a profile named `project` in your `profiles.yml` or use the CI profile as a reference in `.github/profiles.yml`.

3. **Run dbt:**

   ```bash
   cd project
   dbt debug
   dbt build
   dbt test
   ```

### dbt profile placeholders

During `dbt init`, placeholder values were used for the profile configuration (e.g. account, user, role, warehouse, database, schema, threads, etc.).
**You must replace all placeholder values with real connection details before running dbt in any environment.**

By default, the example profile is configured for **Snowflake** (following common enterprise best practices), but:

- **The project itself is adapter-agnostic** – it will work with any supported dbt adapter (Snowflake, Postgres, BigQuery, DuckDB, etc.).
- To use a different warehouse/adapter, simply adjust the profile in `~/.dbt/profiles.yml` (or your configured profiles directory) according to the official dbt docs: `https://docs.getdbt.com/docs/configure-your-profile`.

After you update the placeholders and install dependencies into your environment, you can validate and run the project as shown in the **Quick start** section.

### Project highlights

- **Layered models**: configured in `project/dbt_project.yml` under `models: project:`.
- **Contracts and expectations example**:
  - Model: `project/models/staging/stg_example_orders.sql`
  - Schema + tests: `project/models/staging/stg_example_orders.yml` (including `dbt_expectations` tests).
- **Unit test example**:
  - `project/tests/unit/stg_example_orders_unit.yml`
- **Query tagging per layer**:
  - See `set_query_tag` wiring in `project/dbt_project.yml`.
- **Codegen helpers**:
  - `project/analyses/codegen/generate_model_yaml.sql`
  - `project/analyses/codegen/generate_unit_test_template.sql`

### Recommended ecosystem add-ons

- **dbt_orphan** – automatic cleanup of orphaned tables in dbt-managed schemas.  
  - Already included (commented example hook) via [`Matts52/dbt_orphan`](https://hub.getdbt.com/Matts52/dbt_orphan/latest/).  
  - Start with `dry_run=true` and an explicit list of schemas; only enable dropping after reviewing results.
- **Data quality & observability** around this starter:
  - **dbt-expectations** (already wired in) for richer tests directly in dbt.
  - **re_data** or **Soda Core** if you want separate monitoring/anomaly dashboards on top of dbt runs.
- **Local dev & experimentation**:
  - **DuckDB** as an additional dev target for cheap local iteration before running on Snowflake.
- **Orchestration & ingestion**:
  - Tools like **Dagster/Prefect** (for orchestration) or **dlt/Meltano** (for ingestion) pair well with this dbt starter but live outside this repo.

### Using this starter in your organisation

You will usually:

1. **Clone and rename**  
   - Clone this repo as a new project for your org.  
   - Optionally rename the dbt project from `project` to your internal name (update `project/dbt_project.yml`, profiles, and CI if you do).

2. **Wire up profiles and CI secrets**  
   - Configure your local `profiles.yml` (Snowflake or another adapter).  
   - In CI, set the required `DBT_SNOWFLAKE_*` (or equivalent) environment variables used by `.github/profiles.yml`.

3. **Enable local safety rails**  
   - Install pre‑commit: `pip install pre-commit && pre-commit install`.  
   - This ensures linting, YAML validation, and secret scanning run before each commit.

4. **Adopt CODEOWNERS and PR template**  
   - Update `.github/CODEOWNERS` with your real teams.  
   - Use the provided PR template to enforce review and testing discipline.

5. **Start modeling using the patterns**  
   - Use `stg_example_orders` as a reference for contracts + tests.  
   - Copy its structure when creating new models in `staging`, `intermediate`, and `marts`.  
   - Use the codegen analyses to generate `schema.yml` and unit test templates.

For contribution guidelines, detailed conventions, and recommended workflow, see `CONTRIBUTING.md`.
