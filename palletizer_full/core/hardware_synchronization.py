"""
Hardware Synchronisation Module
================================

Coordinates clock synchronisation across sensors and actuators.
In a palletiser this ensures that conveyor belts, robots and
sensors stay in sync.
"""

from __future__ import annotations

import logging
import time


class HardwareSynchroniser:
    """Synchronise hardware clocks.

    Maintains a reference timestamp and computes offsets for each
    registered device.
    """

    def __init__(self) -> None:
        self._reference_time: float = time.monotonic()
        self._offsets: dict[str, float] = {}
        self._logger = logging.getLogger(self.__class__.__name__)

    def register_device(self, device_id: str, device_time: float) -> None:
        """Register a device and compute its clock offset."""
        offset = time.monotonic() - device_time
        self._offsets[device_id] = offset
        self._logger.debug("Device %s offset: %.6f s", device_id, offset)

    def get_offset(self, device_id: str) -> float:
        """Return the clock offset for a registered device."""
        return self._offsets.get(device_id, 0.0)

    def synchronised_time(self, device_id: str, device_time: float) -> float:
        """Convert a device timestamp to the reference clock."""
        return device_time + self.get_offset(device_id)

    def reset(self) -> None:
        """Reset the reference time and clear all offsets."""
        self._reference_time = time.monotonic()
        self._offsets.clear()
