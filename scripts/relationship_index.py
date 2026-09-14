from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

RELATIONSHIP_DIR = ROOT / "hardware" / "relationships"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def build_relationship_index():
    index = {}

    relationship_files = sorted(
        RELATIONSHIP_DIR.glob("*.yaml")
    )

    for path in relationship_files:
        data = load_yaml(path)

        source = data.get("source")
        target = data.get("target")
        relationship_type = data.get("type")
        details = data.get("details", {})

        if not source or not target:
            continue

        key = (source, target)

        index.setdefault(key, []).append(
            {
                "type": relationship_type,
                "details": details
            }
        )

    return index


def find_relationship(source, target, index):
    return index.get((source, target), [])


if __name__ == "__main__":
    index = build_relationship_index()

    print(
        f"Indexed {sum(len(v) for v in index.values())} "
        "relationship record(s)."
    )
    print()

    for (source, target), relationships in index.items():
        for relationship in relationships:
            protocol = relationship["details"].get(
                "protocol",
                "unspecified"
            )

            print(
                f"{source} → {target} "
                f"({relationship['type']}, {protocol})"
            )