# ACS PROJECT BE

## AI-Driven Hardware-Aware Self-Coding Robotics Framework

**ACS PROJECT BE** is a hardware-aware AI robotics framework that converts natural-language robot tasks into validated executable programs for the physical hardware actually available to the robot.

The core idea is simple:

> **The system must understand the available hardware and its capabilities before generating robot code.**

This prevents the AI from generating code that depends on sensors, actuators, interfaces, or other hardware that does not actually exist.

---

## Core Pipeline

```text
Natural Language Task
        ↓
Task Representation
        ↓
Hardware Knowledge
        ↓
Capability Analysis
        ↓
Feasibility & Constraint Checking
        ↓
Task Planning
        ↓
Hardware Abstraction Layer
        ↓
Code Generation
        ↓
Compilation & Validation
        ↓
Deployment
        ↓
Physical Robot
```

---

## Initial Target

The initial MVP targets an **ESP32-based robotics platform** with a controlled hardware inventory.

### Technology Stack

* ESP32-based robotics platform
* Python backend
* C/C++ embedded firmware
* Structured YAML hardware knowledge records
* JSON Schema validation
* Deterministic hardware validation
* Hardware relationship modelling
* Hardware capability modelling
* Hardware-aware feasibility checking
* Hardware abstraction layer
* AI/LLM integration in later stages
* Automated code generation in later stages
* Physical robot validation in later stages

---

# Hardware Knowledge Architecture

ACS does not treat hardware as a simple list of components.

The hardware knowledge base is divided into multiple layers:

```text
                    HARDWARE KNOWLEDGE
                           │
            ┌──────────────┼──────────────┐
            ↓              ↓              ↓
       COMPONENTS     RELATIONSHIPS   CAPABILITIES
            │              │              │
       What is it?    How does it     What can it
                      interact?          do?
            │              │              │
            └──────────────┼──────────────┘
                           ↓
                  FEASIBILITY ENGINE
```

### Components

Components describe the physical hardware available to the system.

Example:

```text
TCS34725
BNO085
TF-Luna
SG90
NEMA17
ESP32 DevKit
```

### Relationships

Relationships describe how hardware components interact or connect.

Examples:

```text
ESP32 → I2C → TCS34725

ESP32 → PWM → SG90

NEMA17 → driven by → A4988

TB6612FNG → drives → DC Geared Motor
```

### Capabilities

Capabilities describe what the hardware can actually do.

Examples:

```text
TCS34725
    ↓
color_detection

TF-Luna
    ↓
distance_measurement

BNO085
    ↓
orientation
acceleration_measurement
angular_velocity_measurement

SG90
    ↓
angular_actuation

NEMA17
    ↓
stepper_rotation
```

This abstraction allows ACS to reason about **requirements instead of component names**.

For example:

```text
User:
"Detect the red object."

        ↓

Required capability:
color_detection

        ↓

Available provider:
TCS34725

        ↓

Feasibility:
POSSIBLE
```

If the user asks for something requiring a capability that is unavailable:

```text
User:
"Take a picture of the object."

        ↓

Required capability:
image_capture

        ↓

Available hardware:
No camera capability

        ↓

Feasibility:
NOT POSSIBLE
```

---

# MVP Hardware Knowledge Base

The current MVP contains **20 validated hardware components**.

```text
20 Components
      +
20 Relationships
      +
18 Capabilities
```

### Component Categories

The hardware knowledge base currently covers:

* Controllers
* Sensors
* Displays
* Drivers
* Actuators
* Inputs
* Outputs
* Power/control-related hardware
* Communication/interface-related hardware
* Mechanical hardware

---

# Validation Architecture

ACS uses machine-readable schemas and deterministic validators to prevent invalid hardware knowledge from entering the system.

```text
YAML Knowledge Record
        ↓
JSON Schema Validation
        ↓
Cross-Reference Validation
        ↓
Accepted / Rejected
```

### Component Validation

Current result:

```text
20/20 components validated
0 validation errors
```

### Relationship Validation

Current result:

```text
20/20 relationships validated
0 validation errors
```

### Capability Validation

Current result:

```text
18/18 capabilities validated
0 validation errors
0 provider mismatches
```

Capability validation performs two levels of checking:

1. JSON Schema validation
2. Provider validation against the existing component knowledge base

For example:

```yaml
providers:
  - tcs34725
```

is accepted only when `tcs34725` exists as a valid component ID.

---

# Validation Testing

The validators are also tested using intentional failure and recovery cases.

Example:

```text
Valid capability
      ↓
Introduce invalid category
      ↓
Validator rejects record
      ↓
Restore valid category
      ↓
Validator passes
```

This verifies that validation is actively enforcing the schema rather than simply reporting success.

---

# Repository Structure

Current repository architecture:

```text
ACS-BE-PROJECT/
│
├── backend/
│
├── config/
│
├── firmware/
│
├── hardware/
│   │
│   ├── components/
│   │   ├── actuators/
│   │   ├── controllers/
│   │   ├── displays/
│   │   ├── drivers/
│   │   ├── inputs/
│   │   ├── outputs/
│   │   └── sensors/
│   │       ├── distance/
│   │       ├── environment/
│   │       └── proximity/
│   │
│   ├── relationships/
│   │
│   ├── capabilities/
│   │
│   └── schemas/
│       ├── component.schema.json
│       ├── relationship.schema.json
│       └── capability.schema.json
│
├── scripts/
│   ├── validate_component.py
│   ├── validate_relationship.py
│   └── validate_capability.py
│
└── README.md
```

---

# Development Progress

The project is being developed incrementally.

```text
Step 1  ✅ Freeze MVP Hardware Universe
Step 2  ✅ Repository Architecture
Step 3  ✅ Component Schema
Step 4  ✅ Hardware Component Knowledge Base
Step 5  ✅ Hardware Relationship Model
Step 6  ✅ Hardware Capability Model
Step 7  ⏭️ Feasibility Engine
Step 8  ⏭️ Task Representation
Step 9  ⏭️ Task Planning
Step 10 ⏭️ Hardware Abstraction Layer
Step 11 ⏭️ LLM Integration
Step 12 ⏭️ Code Generation
Step 13 ⏭️ Compilation & Validation
Step 14 ⏭️ Physical Robot Testing
Step 15 ⏭️ Automated Deployment
```

---

# Current Status

## Completed

### Step 1 — MVP Hardware Universe

The initial hardware inventory was frozen to provide a controlled environment for deterministic reasoning.

### Step 2 — Repository Architecture

The repository was structured into separate areas for:

* Backend
* Firmware
* Configuration
* Hardware knowledge
* Validation scripts

### Step 3 — Component Schema

A JSON Schema was created to define the structure and constraints of hardware component records.

### Step 4 — Hardware Knowledge Base

20 physical hardware components were documented using structured YAML records.

Validation result:

```text
20/20 ✅
```

### Step 5 — Hardware Relationships

A relationship schema, relationship records, and a deterministic relationship validator were created.

Validation result:

```text
20/20 ✅
```

Failure and recovery testing was also completed.

### Step 6 — Capability Model

A capability schema, 18 capability records, and a capability validator were created.

Validation result:

```text
18/18 ✅
```

The capability validator also verifies that every declared provider exists in the component knowledge base.

---

# Project Principle

The system must reason about the hardware that **actually exists** before generating executable robot code.

ACS should never assume that hardware is available simply because an LLM knows that such hardware exists.

If a requested task requires unavailable hardware, the system should explicitly identify the missing capability or hardware dependency.

```text
Available Hardware
        ↓
Available Capabilities
        ↓
User Requirement
        ↓
Feasibility Analysis
        ↓
Possible / Impossible
```

---

# Engineering Philosophy

The project follows several core principles:

### Hardware-Aware

Generated solutions must respect the physical hardware available to the robot.

### Deterministic Where Possible

Hardware validation and feasibility decisions should be based on structured knowledge rather than uncontrolled LLM assumptions.

### Modular

Components, relationships, capabilities, planning, code generation, and deployment are separate layers.

### Machine-Readable

Hardware knowledge is represented using structured YAML and validated using JSON Schema.

### Extensible

New components and capabilities can be added without redesigning the entire system.

### Safety Through Validation

Invalid hardware knowledge should be rejected before it can influence downstream planning or code generation.

---

# Long-Term Goal

The long-term goal of ACS is to enable a user to describe a robotics task in natural language:

```text
"Detect the red object and move the robotic arm toward it."
```

and have ACS automatically:

```text
Natural Language
        ↓
Understand Task
        ↓
Determine Required Capabilities
        ↓
Check Available Hardware
        ↓
Check Hardware Relationships
        ↓
Determine Feasibility
        ↓
Plan Actions
        ↓
Generate Hardware-Specific Code
        ↓
Compile & Validate
        ↓
Deploy to ESP32
        ↓
Execute on Physical Robot
```

The key difference from a generic code-generation system is that ACS is designed to understand the **physical constraints of the target robot before producing executable code**.

---

## Current Milestone

```text
╔══════════════════════════════════════╗
║     HARDWARE KNOWLEDGE FOUNDATION    ║
╠══════════════════════════════════════╣
║ Components       20/20 ✅            ║
║ Relationships    20/20 ✅            ║
║ Capabilities     18/18 ✅            ║
║ Schema Validation       ✅            ║
║ Cross-Reference Checks  ✅            ║
║ Failure Testing         ✅            ║
║ Recovery Testing        ✅            ║
╚══════════════════════════════════════╝
```

**Current stage: Hardware Knowledge Foundation complete**

**Next major milestone: Feasibility Engine**
