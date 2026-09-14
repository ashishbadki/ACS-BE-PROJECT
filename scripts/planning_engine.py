"""
ACS Hardware-Aware Planning Engine

Step 8 of the ACS project.

The planning engine consumes a hardware request, delegates feasibility
reasoning to the Step 7 feasibility engine, and produces a structured
hardware-aware build plan.
"""

from __future__ import annotations

import json
from typing import Any

from feasibility_engine import (
    build_capability_index,
    build_relationship_index,
    check_hardware_feasibility,
)


def build_hardware_plan(
    controller: str,
    required_capabilities: list[str],
) -> dict[str, Any]:
    """
    Build a hardware-aware plan from a controller and required capabilities.

    Feasibility reasoning is delegated to the existing Step 7 engine.
    """

    capability_index = build_capability_index()
    relationship_index = build_relationship_index()

    feasibility = check_hardware_feasibility(
        required_capabilities=required_capabilities,
        controller_id=controller,
        capability_index=capability_index,
        relationship_index=relationship_index,
    )

    hardware = _build_hardware_list(
        controller=controller,
        feasibility=feasibility,
    )

    steps = _build_steps(
        controller=controller,
        hardware=hardware,
        required_capabilities=required_capabilities,
        feasible=feasibility["feasible"],
    )

    return {
        "request": {
            "controller": controller,
            "required_capabilities": required_capabilities,
        },
        "feasibility": {
            "feasible": feasibility["feasible"],
            "matched_capabilities": feasibility["matched_capabilities"],
            "missing_capabilities": feasibility["missing_capabilities"],
        },
        "hardware_paths": feasibility.get("hardware_paths", []),
        "hardware": hardware,
        "steps": steps,
    }


def _build_hardware_list(
    controller: str,
    feasibility: dict[str, Any],
) -> list[dict[str, str]]:
    """
    Convert structured feasibility paths into the hardware section
    of the plan.

    Example:

        esp32_devkit -> a4988 -> nema17

    becomes three hardware entries while preserving the dependency
    chain discovered by the feasibility engine.
    """

    hardware = [
        {
            "component_id": controller,
            "role": "controller",
        }
    ]

    if not feasibility["feasible"]:
        return hardware

    seen_components = {controller}

    for path in feasibility.get("hardware_paths", []):
        for component_id in path:
            if component_id in seen_components:
                continue

            hardware.append(
                {
                    "component_id": component_id,
                    "role": _infer_component_role(component_id),
                }
            )

            seen_components.add(component_id)

    return hardware


def _infer_component_role(component_id: str) -> str:
    """
    Infer a simple planning role from a component ID.

    This deterministic MVP mapping can later be replaced by information
    read directly from the hardware component knowledge base.
    """

    role_map = {
        "nema17": "stepper_motor",
        "a4988": "stepper_driver",
        "mg90s": "servo_motor",
        "sg90": "servo_motor",
        "tb6612fng": "motor_driver",
        "hc_sr04": "distance_sensor",
        "tf_luna": "distance_sensor",
        "dht22": "environment_sensor",
        "bno085": "imu",
        "tcs34725": "color_sensor",
        "e18_d80nk": "proximity_sensor",
        "oled_0_9_ssd1306": "display",
        "led": "indicator",
        "ws2812b": "addressable_led",
        "active_buzzer": "buzzer",
        "relay_5v": "relay",
        "potentiometer": "analog_input",
        "push_button": "digital_input",
    }

    return role_map.get(component_id, "hardware_component")


def _build_steps(
    controller: str,
    hardware: list[dict[str, str]],
    required_capabilities: list[str],
    feasible: bool,
) -> list[dict[str, Any]]:
    """Generate an ordered hardware build sequence."""

    if not feasible:
        return [
            {
                "step": 1,
                "action": (
                    "Resolve missing hardware capabilities before "
                    "building the requested system."
                ),
            }
        ]

    steps: list[dict[str, Any]] = [
        {
            "step": 1,
            "action": f"Initialize {controller} controller.",
        }
    ]

    step_number = 2

    for item in hardware:
        if item["component_id"] == controller:
            continue

        steps.append(
            {
                "step": step_number,
                "action": (
                    f"Connect and initialize {item['component_id']} "
                    f"as the {item['role']}."
                ),
            }
        )

        step_number += 1

    for capability in required_capabilities:
        steps.append(
            {
                "step": step_number,
                "action": f"Configure hardware for {capability}.",
            }
        )

        step_number += 1

    steps.append(
        {
            "step": step_number,
            "action": "Execute the requested hardware operation.",
        }
    )

    return steps


def main() -> None:
    """Run a small Step 8 demonstration."""

    controller = "esp32_devkit"

    required_capabilities = [
        "stepper_rotation",
    ]

    plan = build_hardware_plan(
        controller=controller,
        required_capabilities=required_capabilities,
    )

    print("ACS Hardware-Aware Planning Engine")
    print("==================================")
    print()

    print(f"Controller: {controller}")

    print(
        "Required capabilities: "
        + ", ".join(required_capabilities)
    )

    print()

    if plan["feasibility"]["feasible"]:
        print("Overall result: FEASIBLE")
    else:
        print("Overall result: NOT FEASIBLE")

    print()

    print("Hardware Paths:")

    for path in plan["hardware_paths"]:
        print(
            "- " + " -> ".join(path)
        )

    print()

    print("Hardware:")

    for item in plan["hardware"]:
        print(
            f"- {item['component_id']} "
            f"({item['role']})"
        )

    print()

    print("Plan:")

    for step in plan["steps"]:
        print(
            f"{step['step']}. "
            f"{step['action']}"
        )

    print()

    print("Structured JSON Plan:")

    print(
        json.dumps(
            plan,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
    