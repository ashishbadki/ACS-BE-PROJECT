import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]

CAPABILITY_DIR = ROOT / "hardware" / "capabilities"
COMPONENT_DIR = ROOT / "hardware" / "components"
SCHEMA_FILE = ROOT / "hardware" / "schemas" / "capability.schema.json"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_component_ids():
    component_ids = set()

    for path in COMPONENT_DIR.rglob("*.yaml"):
        data = load_yaml(path)

        identity = data.get("identity", {})
        component_id = identity.get("id")

        if component_id:
            component_ids.add(component_id)

    return component_ids


def validate_capabilities():
    schema = load_json(SCHEMA_FILE)
    validator = Draft202012Validator(schema)

    component_ids = get_component_ids()

    capability_files = sorted(CAPABILITY_DIR.glob("*.yaml"))

    if not capability_files:
        print("❌ No capability files found.")
        return False

    print(f"Found {len(capability_files)} capability record(s).")
    print()

    all_valid = True

    for path in capability_files:
        try:
            data = load_yaml(path)

            errors = sorted(
                validator.iter_errors(data),
                key=lambda error: list(error.path)
            )

            provider_errors = []

            providers = data.get("providers", [])

            for provider in providers:
                if provider not in component_ids:
                    provider_errors.append(
                        f"provider '{provider}' does not match any component ID"
                    )

            if errors or provider_errors:
                all_valid = False

                print(f"❌ {path.name}")

                for error in errors:
                    location = ".".join(str(part) for part in error.path)
                    if location:
                        print(f"   {location} → {error.message}")
                    else:
                        print(f"   {error.message}")

                for error in provider_errors:
                    print(f"   providers → {error}")

                print()

            else:
                capability_id = data["identity"]["id"]
                capability_name = data["identity"]["name"]

                print(
                    f"✅ {capability_name} ({capability_id})"
                )

        except yaml.YAMLError as error:
            all_valid = False
            print(f"❌ {path.name}")
            print(f"   YAML parsing error → {error}")
            print()

        except Exception as error:
            all_valid = False
            print(f"❌ {path.name}")
            print(f"   Unexpected error → {error}")
            print()

    print()

    if all_valid:
        print("✅ All capabilities passed validation.")
    else:
        print("❌ Capability validation failed.")

    return all_valid


if __name__ == "__main__":
    success = validate_capabilities()
    raise SystemExit(0 if success else 1)