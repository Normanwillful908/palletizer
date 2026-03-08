"""
Orchestrator for the Palletiser
===============================

The :class:`PalletiserOrchestrator` instantiates and wires together
all subsystems: sensor IO, processing, planning, motion control,
gripper control, power and thermal management, hazard detection and
communication.  It runs these subsystems in a deterministic loop
via the :class:`ExecutionStack`.

Usage::

    from palletizer_full.orchestrator import PalletiserOrchestrator

    config = Config()
    robot = MyRobotSDKInterface()  # implements RobotInterface
    orchestrator = PalletiserOrchestrator(config, robot)
    orchestrator.run()
"""

from __future__ import annotations

import logging
import time
from typing import Any

from .config import Config
from .control.gripper_controller import GripperController
from .control.motion_controller import MotionController, RobotInterface
from .core.communication import CommunicationInterface
from .core.concurrency_management import ReentrantLock
from .core.consistency_verification import ConsistencyVerifier
from .core.execution_stack import ExecutionStack
from .core.fault_detection import FaultDetector
from .core.hazard_manager import HazardManager
from .core.memory_management import MemoryManager
from .perception.sensor_io import SensorIO
from .perception.sensor_processing import SensorProcessor
from .planning.mission_planner import MissionPlanner
from .planning.pattern_manager import PatternManager
from .power.battery_management import BatteryManager
from .power.thermal_management import ThermalManager


class PalletiserOrchestrator:
    """High-level orchestrator for the palletising cell."""

    def __init__(self, config: Config, robot: RobotInterface) -> None:
        self.config = config

        # Subsystems
        self.memory = MemoryManager(config.total_memory_bytes)
        self.hazard_manager = HazardManager(config)
        self.fault_detector = FaultDetector()
        self.consistency = ConsistencyVerifier()
        self.communication = CommunicationInterface(config)
        self.battery = BatteryManager(
            config.battery_capacity_wh,
            config.low_battery_threshold,
        )
        self.thermal = ThermalManager(
            config.max_temperature_c,
            config.cooling_hysteresis_c,
        )
        self.sensor_io = SensorIO()
        self.sensor_processor = SensorProcessor()
        self.pattern_manager = PatternManager()
        self.planner = MissionPlanner(self.pattern_manager)

        # Robot motion and gripper
        default_velocities = tuple(1.0 for _ in robot.get_joint_positions())
        self.motion = MotionController(robot, default_velocities)
        self.gripper = GripperController(
            close_fn=lambda: None,
            open_fn=lambda: None,
            read_pressure_fn=None,
        )

        # Concurrency primitive protecting shared state
        self._lock = ReentrantLock()
        self._logger = logging.getLogger(self.__class__.__name__)

        # Execution stack
        self._stack = ExecutionStack(
            config=self.config,
            on_cycle=self._on_cycle,
            on_health_check=self._collect_metrics,
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, cycles: int | None = None) -> None:
        """Start the main control loop."""
        self.communication.connect()
        self._stack.run(cycles)

    def add_order(self, sku: str, quantity: int) -> None:
        """Add a new palletising order to the planner."""
        with self._lock:
            self.planner.add_order(sku, quantity)

    # ------------------------------------------------------------------
    # Internal callbacks invoked by ExecutionStack
    # ------------------------------------------------------------------

    def _on_cycle(self, dt: float) -> None:
        """Perform one control cycle."""
        with self._lock:
            # 1. Poll sensors
            raw = self.sensor_io.read_all()
            processed = self.sensor_processor.process(raw)

            # 2. Update power and thermal subsystems
            self.battery.update(current_draw_w=100.0)
            self.thermal.update()

            # 3. Evaluate hazards
            hazard_inputs: dict[str, Any] = {
                "proximity": processed.get("proximity"),
                "faults": self.fault_detector.get_active_faults(),
                "high_voltage": None,
                "gas": None,
                "radiation": None,
            }
            self.hazard_manager.update(hazard_inputs)

            # 4. If safe and there is a pending order, perform a task
            if self.hazard_manager.is_safe() and self.planner.has_next_task():
                task = self.planner.next_task()
                if task:
                    picked = self.gripper.pick()
                    if not picked:
                        self.fault_detector.report_fault("gripper_pick_failure")
                        return
                    time.sleep(0.01)
                    self.gripper.release()

            # 5. Fault handling: if SOC is low, trigger a fault
            if self.battery.is_low():
                self.fault_detector.report_fault("low_battery")

    def _collect_metrics(self) -> dict[str, Any]:
        """Collect telemetry and health metrics."""
        metrics: dict[str, Any] = {}
        metrics.update(self.battery.telemetry())
        metrics.update(self.thermal.telemetry())
        metrics["memory_ok"] = self.memory.check_health()
        metrics["faults"] = list(self.fault_detector.get_active_faults())
        metrics["hazards"] = self.hazard_manager.current_hazards()
        self.communication.send_telemetry(metrics)
        return metrics
