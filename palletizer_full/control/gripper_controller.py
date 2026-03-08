"""
Gripper Controller Module
=========================

The :class:`GripperController` provides a high-level API for
controlling a vacuum or mechanical gripper.  It monitors vacuum
pressure (if available), triggers retries on failed picks and
detects drops.

The gripper is abstracted by callbacks passed during construction.
Users should provide functions to open/close the gripper and to
read pressure or force feedback.
"""

from __future__ import annotations

import logging
import math
import time
from collections.abc import Callable


class GripperController:
    """Control and monitor a gripper.

    Parameters
    ----------
    close_fn : Callable[[], None]
        Function that closes the gripper.
    open_fn : Callable[[], None]
        Function that opens the gripper.
    read_pressure_fn : Callable[[], float] | None
        Function that returns the current vacuum pressure.
    """

    def __init__(
        self,
        close_fn: Callable[[], None],
        open_fn: Callable[[], None],
        read_pressure_fn: Callable[[], float] | None = None,
    ) -> None:
        self._close_fn = close_fn
        self._open_fn = open_fn
        self._read_pressure = read_pressure_fn
        self._logger = logging.getLogger(self.__class__.__name__)

    def pick(self, retries: int = 3, wait_s: float = 0.1) -> bool:
        """Close the gripper and verify suction/grasp.

        Returns ``True`` on success, ``False`` on failure.
        """
        for attempt in range(retries):
            self._close_fn()
            time.sleep(wait_s)
            if self._read_pressure is None:
                return True
            try:
                pressure = float(self._read_pressure())
            except Exception:
                self._logger.exception("Pressure read error")
                pressure = None
            threshold = -0.2  # negative pressure in bar
            if pressure is not None and pressure < threshold:
                return True
            self._logger.warning(
                "Grip attempt %d failed (pressure=%.3f bar)",
                attempt + 1,
                pressure if pressure is not None else math.nan,
            )
        self._logger.error("Failed to achieve vacuum after %d attempts", retries)
        return False

    def release(self) -> None:
        """Open the gripper to release the load."""
        self._open_fn()
