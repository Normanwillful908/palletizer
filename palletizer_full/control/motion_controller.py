"""
Motion Controller Module
========================

The :class:`MotionController` orchestrates low-level joint commands
to the robot arm.  It delegates actual actuation to an injected
:class:`RobotInterface`, allowing you to simulate the robot or swap
hardware without changing the rest of the stack.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Iterable

from .joint_synchronization import synchronise_velocities


class RobotInterface:
    """Abstract base class for robot arm APIs.

    Implement this interface to connect your robot SDK to the
    palletiser control stack.
    """

    def get_joint_positions(self) -> tuple[float, ...]:
        """Return current joint positions."""
        raise NotImplementedError

    def command_joint_positions(self, positions: tuple[float, ...]) -> None:
        """Command the robot to move to *positions*."""
        raise NotImplementedError

    def execute_trajectory(
        self,
        trajectory: list[tuple[float, ...]],
        dt: float,
    ) -> None:
        """Execute a trajectory at a fixed time interval *dt*."""
        raise NotImplementedError


class MotionController:
    """High-level motion controller for a palletising robot arm."""

    def __init__(
        self,
        robot: RobotInterface,
        max_velocities: tuple[float, ...],
    ) -> None:
        self._robot = robot
        self._max_velocities = max_velocities
        self._logger = logging.getLogger(self.__class__.__name__)

    def move_to(self, target: tuple[float, ...], duration: float = 2.0) -> None:
        """Move the robot to *target* over *duration* seconds."""
        current = self._robot.get_joint_positions()
        if len(current) != len(target):
            msg = "Target joint tuple length mismatch"
            raise ValueError(msg)

        trajectory = [current, target]
        synced = synchronise_velocities(trajectory, self._max_velocities)
        steps = max(int(duration / 0.1), 1)
        for i in range(1, steps + 1):
            alpha = i / steps
            interp = tuple(
                p + alpha * (t - p) for p, t in zip(synced[0], synced[-1], strict=False)
            )
            self._robot.command_joint_positions(interp)
            time.sleep(duration / steps)
        self._robot.command_joint_positions(target)

    def execute_trajectory(
        self,
        trajectory: Iterable[tuple[float, ...]],
        dt: float,
    ) -> None:
        """Execute a pre-computed joint trajectory."""
        positions = list(trajectory)
        if not positions:
            return
        synced = synchronise_velocities(positions, self._max_velocities)
        for pos in synced:
            self._robot.command_joint_positions(pos)
            time.sleep(dt)
