"""
Sensor IO Module
================

The :class:`SensorIO` class is the entry point for reading raw data
from cameras, lidars, proximity sensors and other devices.  In this
reference implementation it returns placeholder data; replace the
``read_all`` method with calls to your sensor SDKs.
"""

from __future__ import annotations

import logging
from typing import Any


class SensorIO:
    """Read raw sensor data from hardware devices."""

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def read_all(self) -> dict[str, Any]:
        """Poll all sensors and return a dictionary of raw readings.

        Override this method to integrate real sensor hardware.
        """
        return {
            "proximity": 1.0,
            "box_present": False,
            "weight_kg": 0.0,
        }
