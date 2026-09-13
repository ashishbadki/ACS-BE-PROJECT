# ACS PROJECT BE

## AI-Driven Hardware-Aware Self-Coding Robotics Framework

ACS PROJECT BE is a hardware-aware AI robotics framework that converts natural-language robot tasks into validated executable programs for the available physical hardware.

## Core Pipeline

Natural Language
↓
Task Representation
↓
Hardware Knowledge
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

## Initial Target

* ESP32-based robotics platform
* Controlled MVP hardware inventory
* Host-based AI and orchestration
* Python backend
* C/C++ embedded firmware
* Structured hardware descriptions
* Deterministic feasibility checking
* Hardware abstraction layer
* Automated code generation and validation in later stages

## Project Principle

The system must reason about the hardware that actually exists before generating executable robot code.

If a requested task requires hardware that is unavailable, the system should identify the missing capability rather than hallucinating a solution.

## Development Strategy

The project is being developed incrementally:

1. Freeze MVP hardware
2. Create repository architecture
3. Define component schema
4. Build hardware knowledge base
5. Build feasibility engine
6. Integrate LLM
7. Generate ESP32 programs
8. Test on physical hardware
9. Add automated deployment and diagram generation

## Status

Current stage: Repository architecture / Step 2
