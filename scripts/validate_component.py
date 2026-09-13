import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = ROOT / "hardware" / "schemas" / "component.schema.json"
COMPONENTS_PATH = ROOT / "hardware" / "components"


def load_schema():
    with SCHEMA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def find_components():
    return sorted(COMPONENTS_PATH.rglob("*.yaml"))


def validate_component(component_path, validator):
    with component_path.open("r", encoding="utf-8") as file:
        component = yaml.safe_load(file)

    errors = sorted(
        validator.iter_errors(component),
        key=lambda error: list(error.path),
    )

    if errors:
        print(f"❌ {component_path.relative_to(ROOT)}")
        
        for error in errors:
            location = " → ".join(str(item) for item in error.path)

            if location:
                print(f"   - {location}: {error.message}")
            else:
                print(f"   - {error.message}")

        return False

    print(
        f"✅ {component['identity']['name']} "
        f"({component['identity']['id']})"
    )

    return True


def main():
    schema = load_schema()
    validator = Draft202012Validator(schema)

    component_files = find_components()

    if not component_files:
        print("❌ No component YAML files found.")
        raise SystemExit(1)

    print(f"Found {len(component_files)} component(s).")
    print()

    failed = False

    for component_path in component_files:
        if not validate_component(component_path, validator):
            failed = True

    print()

    if failed:
        print("❌ Component validation failed.")
        raise SystemExit(1)

    print("✅ All components passed validation.")


if __name__ == "__main__":
    main()