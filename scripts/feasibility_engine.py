import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]

CAPABILITY_DIR = ROOT / "hardware" / "capabilities"

RELATIONSHIP_DIR = ROOT / "hardware" / "relationships"


def load_yaml(path):
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def build_capability_index():
    index = {}

    capability_files = sorted(
        CAPABILITY_DIR.glob("*.yaml")
    )

    for path in capability_files:
        data = load_yaml(path)

        identity = data.get("identity", {})
        capability_id = identity.get("id")

        if capability_id:
            index[capability_id] = {
                "name": identity.get("name"),
                "providers": data.get("providers", [])
            }

    return index


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


def find_dependencies(
    component_id,
    relationship_index
):
    dependencies = []

    for (source, target), relationships in relationship_index.items():
        if source != component_id:
            continue

        for relationship in relationships:
            if relationship["type"] == "requires":
                dependencies.append(target)

    return dependencies


def can_controller_access(
    controller_id,
    component_id,
    relationship_index
):
    relationships = relationship_index.get(
        (controller_id, component_id),
        []
    )

    return len(relationships) > 0


def check_capability(
    capability_id,
    index
):
    capability = index.get(capability_id)

    if capability is None:
        return {
            "feasible": False,
            "capability": capability_id,
            "providers": [],
            "reason": (
                f"Required capability '{capability_id}' "
                "is not present in the capability knowledge base."
            )
        }

    providers = capability["providers"]

    if not providers:
        return {
            "feasible": False,
            "capability": capability_id,
            "providers": [],
            "reason": (
                f"Capability '{capability_id}' exists, "
                "but has no registered providers."
            )
        }

    return {
        "feasible": True,
        "capability": capability_id,
        "providers": providers,
        "reason": (
            f"Capability '{capability_id}' is provided by "
            f"{', '.join(providers)}."
        )
    }


def check_requirements(
    required_capabilities,
    index
):
    matched_capabilities = []
    missing_capabilities = []
    candidate_components = []
    reasons = []

    for capability_id in required_capabilities:

        result = check_capability(
            capability_id,
            index
        )

        if result["feasible"]:
            matched_capabilities.append(
                capability_id
            )

            candidate_components.extend(
                result["providers"]
            )

        else:
            missing_capabilities.append(
                capability_id
            )

        reasons.append(
            result["reason"]
        )

    candidate_components = sorted(
        set(candidate_components)
    )

    feasible = len(
        missing_capabilities
    ) == 0

    return {
        "feasible": feasible,
        "matched_capabilities": matched_capabilities,
        "missing_capabilities": missing_capabilities,
        "candidate_components": candidate_components,
        "reasons": reasons
    }


def check_provider_with_dependencies(
    provider,
    controller_id,
    relationship_index
):
    direct_relationships = relationship_index.get(
        (controller_id, provider),
        []
    )

    if direct_relationships:
        return {
            "feasible": True,
            "path": [
                controller_id,
                provider
            ],
            "reason": (
                f"{controller_id} has a direct relationship "
                f"with {provider}."
            )
        }

    dependencies = find_dependencies(
        provider,
        relationship_index
    )

    if not dependencies:
        return {
            "feasible": False,
            "path": [],
            "reason": (
                f"No relationship exists between "
                f"{controller_id} and {provider}, "
                "and the provider has no known dependencies."
            )
        }

    for dependency in dependencies:

        if can_controller_access(
            controller_id,
            dependency,
            relationship_index
        ):
            return {
                "feasible": True,
                "path": [
                    controller_id,
                    dependency,
                    provider
                ],
                "reason": (
                    f"{controller_id} can access dependency "
                    f"{dependency}, which is required by {provider}."
                )
            }

    return {
        "feasible": False,
        "path": [],
        "reason": (
            f"{provider} requires "
            f"{', '.join(dependencies)}, "
            f"but {controller_id} has no known relationship "
            "with the required dependency."
        )
    }


def check_hardware_feasibility(
    required_capabilities,
    controller_id,
    capability_index,
    relationship_index
):
    matched_capabilities = []
    missing_capabilities = []
    candidate_components = []
    hardware_paths = []
    reasons = []

    for capability_id in required_capabilities:

        capability = capability_index.get(
            capability_id
        )

        if capability is None:

            missing_capabilities.append(
                capability_id
            )

            reasons.append(
                f"Required capability '{capability_id}' "
                "is not present in the capability knowledge base."
            )

            continue

        compatible_providers = []

        for provider in capability["providers"]:

            provider_result = check_provider_with_dependencies(
                provider,
                controller_id,
                relationship_index
            )

            # IMPORTANT:
            # This must stay INSIDE the provider loop.
            if provider_result["feasible"]:
                compatible_providers.append(
                    provider
                )

        if compatible_providers:

            matched_capabilities.append(
                capability_id
            )
            for provider in compatible_providers:
                provider_result = check_provider_with_dependencies(
                    provider,
                    controller_id,
                    relationship_index
                )

                if provider_result["path"]:
                    hardware_paths.append(
                        provider_result["path"]
                    )

            candidate_components.extend(
                compatible_providers
            )

            relationship_details = []

            for provider in compatible_providers:

                provider_result = check_provider_with_dependencies(
                    provider,
                    controller_id,
                    relationship_index
                )

                relationship_details.append(
                    " → ".join(
                        provider_result["path"]
                    )
                )

            reasons.append(
                f"Capability '{capability_id}' is feasible "
                f"with {controller_id}: "
                f"{', '.join(relationship_details)}."
            )

        else:

            missing_capabilities.append(
                capability_id
            )

            reasons.append(
                f"Capability '{capability_id}' has providers, "
                f"but none have a known relationship with "
                f"{controller_id}."
            )

    candidate_components = sorted(
        set(candidate_components)
    )

    feasible = len(
        missing_capabilities
    ) == 0

    return {
    "feasible": feasible,
    "matched_capabilities": matched_capabilities,
    "missing_capabilities": missing_capabilities,
    "candidate_components": candidate_components,
    "hardware_paths": hardware_paths,
    "reasons": reasons
}


def build_feasibility_result(
    controller_id,
    required_capabilities,
    result
):
    return {
        "request": {
            "controller": controller_id,
            "required_capabilities": required_capabilities
        },
        "result": {
            "feasible": result["feasible"],
            "matched_capabilities": result["matched_capabilities"],
            "missing_capabilities": result["missing_capabilities"],
            "candidate_components": result["candidate_components"],
            "hardware_paths": result["hardware_paths"],
            "reasons": result["reasons"]
        }
    }


if __name__ == "__main__":

    capability_index = build_capability_index()

    relationship_index = build_relationship_index()

    controller_id = "esp32_devkit"

    required_capabilities = [
        "stepper_rotation",
        
    ]

    result = check_hardware_feasibility(
        required_capabilities,
        controller_id,
        capability_index,
        relationship_index
    )

    structured_result = build_feasibility_result(
        controller_id,
        required_capabilities,
        result
    )

    print("Hardware Feasibility Engine")
    print("===========================")
    print()

    print(
        f"Controller: {controller_id}"
    )

    print(
        "Required capabilities: "
        f"{', '.join(required_capabilities)}"
    )

    print()

    for capability_id in result[
        "matched_capabilities"
    ]:
        print(
            f"✅ {capability_id}"
        )

    for capability_id in result[
        "missing_capabilities"
    ]:
        print(
            f"❌ {capability_id}"
        )

    print()

    print(
        "Compatible components: "
        f"{', '.join(result['candidate_components'])}"
    )

    print()

    if result["feasible"]:
        print(
            "✅ Overall result: FEASIBLE"
        )
    else:
        print(
            "❌ Overall result: NOT FEASIBLE"
        )

    print()

    print("Reasons:")

    for reason in result["reasons"]:
        print(
            f"- {reason}"
        )

    print()

    print("Structured JSON Result:")

    print(
        json.dumps(
            structured_result,
            indent=2
        )
    )