"""
Custom Gripper Integration Example
===================================

This example demonstrates how to integrate a custom gripper with
pressure feedback into the palletiser control stack.
"""

from __future__ import annotations

import logging

from palletizer_full.control.gripper_controller import GripperController


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Simulate a vacuum gripper with pressure feedback
    gripper_state = {"closed": False, "pressure": 0.0}

    def close() -> None:
        gripper_state["closed"] = True
        gripper_state["pressure"] = -0.5  # good vacuum

    def open_grip() -> None:
        gripper_state["closed"] = False
        gripper_state["pressure"] = 0.0

    def read_pressure() -> float:
        return gripper_state["pressure"]

    gc = GripperController(
        close_fn=close,
        open_fn=open_grip,
        read_pressure_fn=read_pressure,
    )

    # Attempt a pick
    success = gc.pick(retries=3, wait_s=0.01)
    print(f"Pick result: {'success' if success else 'failed'}")

    # Release
    gc.release()
    print("Released")


if __name__ == "__main__":
    main()
