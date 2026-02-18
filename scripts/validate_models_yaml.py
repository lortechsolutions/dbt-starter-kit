#!/usr/bin/env python3
"""
Validate dbt model YAML documentation using Pydantic.

Enterprise-ready defaults:
- Every schema file must declare `version: 2` at the top level.
- Every model must have: name, description.
- Every model must enforce contracts: `config: contract: enforced: true`.
- Every column must define: name, description, data_type.
- name min length: 1, description min length: 1.

Usage:
  python scripts/validate_models_yaml.py --dbt-root project
  python scripts/validate_models_yaml.py --dbt-root project --changed-only
"""

import argparse
import glob
import pprint
import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator


class DBTModelContract(BaseModel):
    enforced: bool

    @field_validator("enforced")
    def contract_must_be_true(cls, value: bool) -> bool:  # type: ignore[override]
        if value is not True:
            raise ValueError("config.contract.enforced must be true")
        return value


class DBTModelConfig(BaseModel):
    contract: DBTModelContract


class DBTModelColumn(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=5)
    data_type: str = Field(min_length=1)


class DBTModel(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    meta: dict[str, Any] | None = None
    config: DBTModelConfig
    columns: list[DBTModelColumn] = Field(default_factory=list)
    additional_args: dict[str, Any] | None = None


POSTFIX_PATTERN = re.compile(r"_v\d+$")


def iter_model_sql_files(models_dir: Path):
    yield from models_dir.rglob("*.sql")


def ensure_corresponding_yml_exists(models_dir: Path) -> list[str]:
    errors: list[str] = []
    for sql_path in iter_model_sql_files(models_dir):
        base = POSTFIX_PATTERN.sub("", sql_path.stem)
        yml_path = sql_path.with_name(base).with_suffix(".yml")
        if not yml_path.exists():
            errors.append(f"Corresponding YAML file not found for: {sql_path}")
    return errors


def validate_yaml_models_in_file(filename: str) -> list[str]:
    errors: list[str] = []
    with open(filename, encoding="utf-8") as stream:
        try:
            yaml_file = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            errors.append(f"YAML parse error in {filename}: {exc}")
            return errors

    # 1. Ensure top-level version: 2
    top_level = yaml_file or {}
    version = top_level.get("version")
    if version != 2:
        errors.append(f"{filename}: top-level 'version: 2' is required for model schema files.")

    try:
        yaml_models = top_level.get("models", [])
    except Exception:
        # likely sources/exposures/etc
        return errors

    for model in yaml_models:
        try:
            DBTModel(**model)
        except ValidationError as e:
            errors.append(f"ERROR in model: {model.get('name')} in file: {filename}")
            for x in e.errors():
                errors.append(f'- Field "{x["loc"][0]}": {x["type"]}')
                errors.append(f'\t- {x["msg"]}')
    return errors


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--dbt-root",
        required=True,
        help="Path to dbt project root (the folder containing models/).",
    )
    p.add_argument(
        "--changed-only",
        action="store_true",
        help="Only validate YAML files changed in the current git diff (best for CI).",
    )
    args = p.parse_args()

    dbt_root = Path(args.dbt_root).resolve()
    models_dir = dbt_root / "models"
    if not models_dir.exists():
        raise SystemExit(f"models dir does not exist: {models_dir}")

    all_errors: list[str] = []

    all_errors.extend(ensure_corresponding_yml_exists(models_dir))

    if args.changed_only:
        # Conservative: validate any changed .yml under models/
        import subprocess

        proc = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1..HEAD"],
            text=True,
            capture_output=True,
        )
        changed = [
            str(Path(x).resolve())
            for x in proc.stdout.splitlines()
            if x.strip().endswith(".yml") and "/models/" in x.replace("\\", "/")
        ]
        files = changed
    else:
        files = glob.glob(str(models_dir / "**" / "*.yml"), recursive=True)

    for filename in files:
        all_errors.extend(validate_yaml_models_in_file(filename))

    if all_errors:
        print("##############################")
        for e in all_errors:
            print(e)
        print("\nExpected YAML schema for models:")
        pprint.pprint(DBTModel.model_fields, indent=3)
        raise SystemExit("Please update the models specified above.")

    print("OK: dbt model YAML validation passed.")


if __name__ == "__main__":
    main()

