import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATH = (
    ROOT
    / "hardware"
    / "schemas"
    / "feasibility.schema.json"
)


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


schema = load_json(SCHEMA_PATH)

Draft202012Validator.check_schema(schema)


valid_example = {
    "request": {
        "controller": "esp32_devkit",
        "required_capabilities": [
            "stepper_rotation"
        ]
    },
    "result": {
        "feasible": True,
        "matched_capabilities": [
            "stepper_rotation"
        ],
        "missing_capabilities": [],
        "candidate_components": [
            "nema17"
        ],
        "reasons": [
            "Capability 'stepper_rotation' is feasible "
            "with esp32_devkit: "
            "esp32_devkit → a4988 → nema17."
        ]
    }
}


validator = Draft202012Validator(schema)

errors = sorted(
    validator.iter_errors(valid_example),
    key=lambda error: list(error.path)
)


if errors:
    print("❌ Feasibility result failed schema validation.")

    for error in errors:
        location = " → ".join(
            str(item)
            for item in error.path
        )

        if not location:
            location = "root"

        print(
            f"   {location} → {error.message}"
        )

else:
    print("✅ Feasibility schema is valid.")
    print("✅ Engine result passed schema validation.")