"""
Basic Palletising Example
=========================

This example shows how to wire up the palletiser with a dummy robot,
register a stacking pattern and run a short palletising cycle.
"""

from __future__ import annotations

import logging
import time

from palletizer_full.config import Config
from palletizer_full.control.motion_controller import RobotInterface
from palletizer_full.orchestrator import PalletiserOrchestrator


class DummyRobot(RobotInterface):
    """Minimal robot stub for demonstration."""

    def __init__(self, joint_count: int = 6) -> None:
        self._joints = [0.0] * joint_count

    def get_joint_positions(self) -> tuple[float, ...]:
        return tuple(self._joints)

    def command_joint_positions(self, positions: tuple[float, ...]) -> None:
        self._joints = list(positions)

    def execute_trajectory(
        self,
        trajectory: list[tuple[float, ...]],
        dt: float,
    ) -> None:
        for pos in trajectory:
            self.command_joint_positions(pos)
            time.sleep(dt)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    cfg = Config()
    robot = DummyRobot()
    orch = PalletiserOrchestrator(cfg, robot)

    # Register a 3-position layer pattern
    orch.pattern_manager.load_pattern(
        "standard_box",
        [
            (0.0, 0.0, 0.0),
            (0.3, 0.0, 0.0),
            (0.0, 0.4, 90.0),
        ],
    )

    # Queue an order of 6 boxes
    orch.add_order("standard_box", 6)

    # Run 50 control cycles
    orch.run(cycles=50)
    print(f"Completed {orch.planner.completed_count} tasks")


if __name__ == "__main__":
    main()
