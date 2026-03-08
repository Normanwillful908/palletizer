"""Tests for the GripperController."""

from __future__ import annotations

from palletizer_full.control.gripper_controller import GripperController


class TestGripperController:
    """Validate gripper pick/release logic."""

    def test_pick_no_feedback(self) -> None:
        gc = GripperController(close_fn=lambda: None, open_fn=lambda: None)
        assert gc.pick(retries=1, wait_s=0.001) is True

    def test_pick_with_good_pressure(self) -> None:
        gc = GripperController(
            close_fn=lambda: None,
            open_fn=lambda: None,
            read_pressure_fn=lambda: -0.5,
        )
        assert gc.pick(retries=1, wait_s=0.001) is True

    def test_pick_with_bad_pressure(self) -> None:
        gc = GripperController(
            close_fn=lambda: None,
            open_fn=lambda: None,
            read_pressure_fn=lambda: 0.0,
        )
        assert gc.pick(retries=2, wait_s=0.001) is False

    def test_release(self) -> None:
        released = []
        gc = GripperController(
            close_fn=lambda: None,
            open_fn=lambda: released.append(True),
        )
        gc.release()
        assert len(released) == 1
