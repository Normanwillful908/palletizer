"""
Consistency Verification Module
================================

The :class:`ConsistencyVerifier` validates that sensor readings and
actuator states are within expected ranges.  It is used during
commissioning and at runtime to detect calibration drift or hardware
faults.
"""

from __future__ import annotations

import logging


class ConsistencyVerifier:
    """Validate sensor/actuator consistency."""

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.__class__.__name__)

    def verify_range(self, name: str, value: float, low: float, high: float) -> bool:
        """Check that *value* is within [*low*, *high*].

        Returns ``True`` if the value is in range, ``False`` otherwise.
        """
        if low <= value <= high:
            return True
        self._logger.warning(
            "%s out of range: %.3f not in [%.3f, %.3f]",
            name,
            value,
            low,
            high,
        )
        return False

    def verify_monotonic(self, name: str, values: list[float]) -> bool:
        """Check that *values* are strictly increasing.

        Useful for verifying encoder readings or timestamps.
        """
        for i in range(1, len(values)):
            if values[i] <= values[i - 1]:
                self._logger.warning(
                    "%s not monotonic at index %d: %.3f <= %.3f",
                    name,
                    i,
                    values[i],
                    values[i - 1],
                )
                return False
        return True
