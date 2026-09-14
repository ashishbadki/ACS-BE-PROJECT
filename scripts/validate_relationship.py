from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = PROJECT_ROOT / "hardware" / "schemas" / "relationship.schema.json"
RELATIONSHIPS_DIR = PROJECT_ROOT / "hardware" / "relationships"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_schema(path: Path):
    with path.open("r", encoding="utf-8") as file:
        import json
        return json.load(file)


def format_relationship(data):
    return (
        f"{data.get('source', '?')} "
        f"→ {data.get('type', '?')} → "
        f"{data.get('target', '?')}"
    )


def main():
    if not SCHEMA_PATH.exists():
        print(f"❌ Schema not found: {SCHEMA_PATH}")
        sys.exit(1)

    if not RELATIONSHIPS_DIR.exists():
        print(f"❌ Relationships directory not found: {RELATIONSHIPS_DIR}")
        sys.exit(1)

    schema = load_schema(SCHEMA_PATH)
    validator = Draft202012Validator(schema)

    relationship_files = sorted(
        RELATIONSHIPS_DIR.glob("*.yaml")
    )

    if not relationship_files:
        print("❌ No relationship YAML files found.")
        sys.exit(1)

    print(f"Found {len(relationship_files)} relationship(s).\n")

    failed = False

    for path in relationship_files:
        try:
            data = load_yaml(path)
        except Exception as exc:
            print(f"❌ {path.name}")
            print(f"   YAML parsing error: {exc}\n")
            failed = True
            continue

        errors = sorted(
            validator.iter_errors(data),
            key=lambda error: list(error.path)
        )

        if errors:
            failed = True
            print(f"❌ {path.name}")

            for error in errors:
                location = " → ".join(str(x) for x in error.path)

                if location:
                    print(f"   {location}: {error.message}")
                else:
                    print(f"   {error.message}")

            print()
        else:
            print(
                f"✅ {path.name} "
                f"({format_relationship(data)})"
            )

    print()

    if failed:
        print("❌ Relationship validation failed.")
        sys.exit(1)

    print("✅ All relationships passed validation.")


if __name__ == "__main__":
    main()