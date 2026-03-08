"""Tests for the MotionController."""

from __future__ import annotations

import pytest

from palletizer_full.control.motion_controller import MotionController


class TestMotionController:
    """Validate motion controller behaviour with a dummy robot."""

    def test_move_to_updates_joints(self, dummy_robot) -> None:
        mc = MotionController(dummy_robot, (1.0,) * 6)
        target = (0.5,) * 6
        mc.move_to(target, duration=0.1)
        assert dummy_robot.get_joint_positions() == target

    def test_move_to_length_mismatch(self, dummy_robot) -> None:
        mc = MotionController(dummy_robot, (1.0,) * 6)
        with pytest.raises(ValueError, match="mismatch"):
            mc.move_to((0.5, 0.5), duration=0.1)

    def test_execute_empty_trajectory(self, dummy_robot) -> None:
        mc = MotionController(dummy_robot, (1.0,) * 6)
        mc.execute_trajectory([], dt=0.01)  # should not raise

    def test_execute_trajectory(self, dummy_robot) -> None:
        mc = MotionController(dummy_robot, (1.0,) * 6)
        traj = [(0.1,) * 6, (0.2,) * 6]
        mc.execute_trajectory(traj, dt=0.001)
        pos = dummy_robot.get_joint_positions()
        assert all(abs(p - 0.2) < 0.01 for p in pos)
