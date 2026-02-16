## dbt project overview

This folder contains the actual dbt project used by the starter kit.

### Layout

- `models/staging/` – source‑aligned models close to raw data.
- `models/intermediate/` – reusable business logic, joins, enrichments.
- `models/marts/` – final, consumer‑facing models (facts/dimensions, reporting).
- `analyses/codegen/` – helpers for generating model YAML and unit test templates.
- `macros/` – shared macros (`generate_schema_name`, `query_tag`, etc.).
- `tests/unit/` – example unit tests (see `stg_example_orders_unit.yml`).

### Getting started (from this directory)

1. Ensure dependencies and dbt packages are installed (see root `README.md`).
2. Run dbt commands:

   ```bash
   dbt debug
   dbt build
   dbt test
   ```

### Adding a new model

- Choose the right layer (`staging`, `intermediate`, `marts`).
- Create a SQL model and a matching `schema.yml` with:
  - `version: 2`
  - model `name` and `description`
  - `config.contract.enforced: true`
  - `columns` with `name`, `description`, `data_type`
- Add tests (built‑in + optional `dbt_expectations`) and run `dbt build` locally.

For full guidelines, see the root `CONTRIBUTING.md`.
