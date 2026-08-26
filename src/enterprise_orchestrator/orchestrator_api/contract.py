from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ContractValidationError(ValueError):
    """Raised when model output does not satisfy the governed output contract."""


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SCHEMA_PATH = ROOT / "prompts" / "output-contract.schema.json"


def load_output_contract(schema_path: Path = DEFAULT_SCHEMA_PATH) -> dict[str, Any]:
    with schema_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_model_output(
    payload: dict[str, Any], schema_path: Path = DEFAULT_SCHEMA_PATH
) -> None:
    """Validate model output against the repository output contract.

    This intentionally supports only the JSON Schema features used by the
    appliance contract. It avoids introducing a runtime dependency before the
    service stack is selected.
    """

    schema = load_output_contract(schema_path)
    errors = list(_validate_value(payload, schema, "$"))
    if errors:
        raise ContractValidationError("; ".join(errors))


def _validate_value(value: Any, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []
    expected_type = schema.get("type")

    if expected_type and not _matches_type(value, expected_type):
        return [f"{path}: expected {expected_type}, got {type(value).__name__}"]

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']}, got {value!r}")

    if expected_type == "string":
        min_length = schema.get("minLength")
        if min_length is not None and len(value) < min_length:
            errors.append(f"{path}: string shorter than {min_length}")

    if expected_type == "object":
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append(f"{path}: missing required field {field!r}")

        properties = schema.get("properties", {})
        for field, field_value in value.items():
            field_path = f"{path}.{field}"
            if field in properties:
                errors.extend(_validate_value(field_value, properties[field], field_path))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{field_path}: additional properties are not allowed")

    if expected_type == "array":
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                errors.extend(_validate_value(item, item_schema, f"{path}[{index}]"))

    return errors


def _matches_type(value: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(value, dict)
    if expected_type == "array":
        return isinstance(value, list)
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "boolean":
        return isinstance(value, bool)
    return True
