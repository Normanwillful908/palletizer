"""
Entry point for the palletiser control system.

This module instantiates a dummy robot interface and launches the
palletiser orchestrator.  In a production deployment you should
replace :class:`DummyRobot` with an implementation of
:class:`~palletizer_full.control.motion_controller.RobotInterface`
that talks to your robot controller API.
"""

from __future__ import annotations

import logging
import time

from .config import Config
from .control.motion_controller import RobotInterface
from .orchestrator import PalletiserOrchestrator


class DummyRobot(RobotInterface):
    """Minimal robot stub for development and testing."""

    def __init__(self, joint_count: int = 6) -> None:
        self._joints = [0.0] * joint_count

    def get_joint_positions(self) -> tuple[float, ...]:
        return tuple(self._joints)

    def command_joint_positions(self, positions: tuple[float, ...]) -> None:
        self._joints = list(positions)
        logging.debug("Commanded joints: %s", positions)

    def execute_trajectory(
        self,
        trajectory: list[tuple[float, ...]],
        dt: float,
    ) -> None:
        for pos in trajectory:
            self.command_joint_positions(pos)
            time.sleep(dt)


def main() -> None:
    """Run the palletiser with a dummy robot for demonstration."""
    logging.basicConfig(level=logging.INFO)
    cfg = Config()
    robot = DummyRobot()
    orchestrator = PalletiserOrchestrator(cfg, robot)

    # Register a simple pattern for demonstration
    orchestrator.pattern_manager.load_pattern(
        "demo_case",
        [
            (0.0, 0.0, 0.0),
            (0.3, 0.0, 0.0),
            (0.0, 0.4, 90.0),
        ],
    )

    # Add a small order of three cases
    orchestrator.add_order("demo_case", 3)

    # Run a limited number of cycles for demonstration
    orchestrator.run(cycles=100)


if __name__ == "__main__":
    main()
