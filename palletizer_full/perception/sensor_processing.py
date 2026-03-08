"""
Sensor Processing Module
========================

The :class:`SensorProcessor` fuses raw sensor inputs to extract
higher-level information such as box presence, alignment and
orientation.  For a palletiser the perception stack is intentionally
simple; you may add machine-learning-based detection later.
"""

from __future__ import annotations

import logging
from typing import Any


class SensorProcessor:
    """Process and fuse raw sensor readings."""

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def process(self, raw: dict[str, Any]) -> dict[str, Any]:
        """Process raw sensor data and return fused results.

        Parameters
        ----------
        raw : dict
            Raw sensor readings from :class:`SensorIO`.

        Returns
        -------
        dict
            Processed data including ``proximity``, ``box_detected``
            and ``weight_kg``.
        """
        proximity = raw.get("proximity")
        box_present = raw.get("box_present", False)
        weight = raw.get("weight_kg", 0.0)

        return {
            "proximity": proximity,
            "box_detected": bool(box_present) or (weight is not None and weight > 0.1),
            "weight_kg": weight,
        }
