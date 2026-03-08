"""Shared test fixtures for the palletiser test suite."""

from __future__ import annotations

import pytest

from palletizer_full.config import Config
from palletizer_full.control.motion_controller import RobotInterface


class DummyRobot(RobotInterface):
    """Minimal robot stub for tests."""

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


@pytest.fixture()
def config() -> Config:
    """Return a default Config instance."""
    return Config()


@pytest.fixture()
def dummy_robot() -> DummyRobot:
    """Return a 6-joint dummy robot."""
    return DummyRobot()
