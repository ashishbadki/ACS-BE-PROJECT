import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = ROOT / "hardware" / "schemas" / "component.schema.json"
COMPONENT_PATH = (
    ROOT
    / "hardware"
    / "components"
    / "sensors"
    / "bno085.yaml"
)


def main() -> None:
    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        schema = json.load(file)

    with COMPONENT_PATH.open("r", encoding="utf-8") as file:
        component = yaml.safe_load(file)

    validator = Draft202012Validator(schema)

    errors = sorted(
        validator.iter_errors(component),
        key=lambda error: list(error.path),
    )

    if errors:
        print("❌ Component validation failed.")
        print()

        for error in errors:
            location = " → ".join(str(item) for item in error.path)
            print(f"- {location}: {error.message}")

        raise SystemExit(1)

    print("✅ Component validation successful.")
    print(f"Component: {component['identity']['name']}")
    print(f"ID: {component['identity']['id']}")


if __name__ == "__main__":
    main()