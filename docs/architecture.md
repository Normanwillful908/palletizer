# Architecture Guide

This document describes the software architecture of the Palletizer Full Stack. It is intended for engineers who want to understand how the system is structured before extending or deploying it.

## Design Principles

The stack is built on four principles that guide every design decision.

**Hardware agnosticism.** The software never calls a specific robot SDK directly. All hardware interaction goes through abstract interfaces (`RobotInterface` for the arm, callbacks for the gripper, `SensorIO` for sensors). This means you can swap your robot, your gripper or your sensor suite without touching the planning, safety or power management code.

**Deterministic control.** The `ExecutionStack` runs a fixed-rate loop. Every cycle follows the same sequence: poll sensors, update power and thermal state, evaluate hazards, execute tasks, publish telemetry. This predictability is essential for safety certification and debugging.

**Modular composition.** Each package (core, control, perception, planning, power) is self-contained. The `PalletiserOrchestrator` wires them together at startup. You can test any package in isolation by providing mock dependencies.

**Configuration over code.** All tunable parameters are exposed as environment variables. Changing the control frequency, safety margins or battery capacity does not require a code change or a rebuild.

## Package Responsibilities

### core/

Foundational services that every other package depends on. This includes memory management for deterministic allocation, hazard monitoring that aggregates signals from multiple sources, fault detection for tracking and querying system faults, concurrency primitives for thread-safe access to shared state, the communication interface for telemetry publishing, the execution stack that drives the control loop, environment adaptation for adjusting parameters to different factory profiles, consistency verification for validating sensor and actuator readings, and hardware synchronisation for coordinating clocks across devices.

### control/

Low-level motion and actuation. The `RobotInterface` defines the contract that your robot SDK must implement. The `MotionController` provides high-level methods like `move_to` and `execute_trajectory` that handle interpolation and velocity synchronisation. The `GripperController` abstracts vacuum or mechanical grippers with retry logic and pressure feedback.

### perception/

Sensor data acquisition and fusion. `SensorIO` reads raw data from hardware devices. `SensorProcessor` fuses raw readings into structured signals (box detection, proximity, weight) that the planner and hazard manager consume.

### planning/

Task-level intelligence. The `PatternManager` stores and retrieves stacking patterns (lists of x, y, rotation poses). The `MissionPlanner` breaks orders into individual pick-and-place tasks and sequences them through a queue.

### power/

Energy and thermal monitoring. The `BatteryManager` tracks state-of-charge and triggers low-battery alerts. The `ThermalManager` monitors actuator temperatures and activates cooling with hysteresis to avoid rapid cycling.

## Data Flow

```
Sensors ──> SensorIO ──> SensorProcessor ──> HazardManager
                                                  │
                                                  ▼
Orders ──> PatternManager ──> MissionPlanner ──> Orchestrator
                                                  │
                                                  ▼
                                          MotionController ──> RobotInterface
                                          GripperController
                                                  │
                                                  ▼
                                          CommunicationInterface ──> Telemetry
```

## Extending the Stack

To add a new subsystem (for example, a vision-based box detector), create a new module in the appropriate package, define its interface, and wire it into the orchestrator. The deterministic loop in `ExecutionStack` will call your code every cycle through the `on_cycle` callback.
