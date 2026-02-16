### Summary

Describe the goal of this change and the main behavior it introduces or modifies.

### Checklist

- [ ] **Code**: Changes follow project conventions and are reasonably small and reviewable.
- [ ] **dbt**: Models/macros/tests updated as needed and `dbt build` succeeds locally.
- [ ] **Documentation**: `schema.yml` updated with `description` and `meta.owners` for all new/changed models.
- [ ] **Tests**: New models have appropriate tests (e.g. `unique`, `not_null`, relationships).
- [ ] **Ownership**: CODEOWNERS are correctly set for any new paths.
- [ ] **CI**: I have checked that CI workflows (lint, dbt build, metadata validation) are passing or understand any failures.

### Testing

- [ ] `dbt build` (or targeted selection) run locally against the appropriate environment.
- [ ] Additional checks (if relevant): performance, backfill strategy, data quality monitoring, etc.

### Notes for reviewers

Anything that would help reviewers understand tricky parts, trade-offs, or rollout risks.

