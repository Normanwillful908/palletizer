# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-03-08

### Added

- Complete palletiser control stack with six modular packages (core, control, perception, planning, power, orchestrator).
- Hardware-agnostic `RobotInterface` abstraction for connecting any robot arm SDK.
- `GripperController` with retry logic and vacuum pressure feedback.
- `PatternManager` for defining and persisting pallet stacking layouts.
- `MissionPlanner` for order sequencing and task dispatch.
- `HazardManager` aggregating proximity, voltage, gas, radiation and fault signals.
- `FaultDetector` for registering, clearing and querying system faults.
- `BatteryManager` with state-of-charge tracking and low-battery alerts.
- `ThermalManager` with hysteresis-based cooling control.
- `MemoryManager` for deterministic buffer allocation.
- `ExecutionStack` for fixed-rate deterministic control loops.
- `CommunicationInterface` for telemetry publishing.
- Environment-variable-driven configuration via `Config` and `RobotConfig`.
- Comprehensive test suite with 40+ tests.
- Three working examples: basic palletising, custom gripper, monitoring telemetry.
- Docker and docker-compose support.
- GitHub Actions CI/CD with ruff linting and pytest.
- Enterprise and gateway directory placeholders for future extensions.
