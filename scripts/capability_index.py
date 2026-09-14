from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

CAPABILITY_DIR = ROOT / "hardware" / "capabilities"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def build_capability_index():
    index = {}

    capability_files = sorted(CAPABILITY_DIR.glob("*.yaml"))

    for path in capability_files:
        data = load_yaml(path)

        identity = data.get("identity", {})
        capability_id = identity.get("id")
        providers = data.get("providers", [])

        if capability_id:
            index[capability_id] = {
                "name": identity.get("name"),
                "providers": providers
            }

    return index


if __name__ == "__main__":
    index = build_capability_index()

    print(f"Indexed {len(index)} capability record(s).")
    print()

    for capability_id, data in index.items():
        print(f"{capability_id}:")
        print(f"  name: {data['name']}")
        print(f"  providers: {', '.join(data['providers'])}")
        print()
        