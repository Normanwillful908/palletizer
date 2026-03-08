"""
Thermal Management Module
=========================

The :class:`ThermalManager` monitors actuator temperatures and
triggers cooling when thresholds are exceeded.  It applies a
hysteresis strategy to avoid rapid cycling of fans or pumps.
"""

from __future__ import annotations

import logging
from typing import Any


class ThermalManager:
    """Monitor temperatures and control cooling.

    Parameters
    ----------
    max_temp_c : float
        Maximum safe temperature in degrees Celsius.
    hysteresis_c : float
        Temperature difference between activating and deactivating
        cooling.
    """

    def __init__(self, max_temp_c: float = 70.0, hysteresis_c: float = 10.0) -> None:
        self._max_temp = max_temp_c
        self._hysteresis = hysteresis_c
        self._current_temp = 25.0  # ambient default
        self._cooling_active = False
        self._logger = logging.getLogger(self.__class__.__name__)

    def update(self, temperature_c: float | None = None) -> None:
        """Update the current temperature reading.

        If *temperature_c* is ``None``, the manager simulates a
        small temperature increase for demonstration purposes.
        """
        if temperature_c is not None:
            self._current_temp = temperature_c
        else:
            self._current_temp += 0.01  # placeholder drift

        if self._current_temp >= self._max_temp:
            if not self._cooling_active:
                self._logger.warning(
                    "Temperature %.1f C exceeds max %.1f C — activating cooling",
                    self._current_temp,
                    self._max_temp,
                )
            self._cooling_active = True
        elif self._current_temp <= self._max_temp - self._hysteresis:
            if self._cooling_active:
                self._logger.info("Temperature normalised — deactivating cooling")
            self._cooling_active = False

    @property
    def is_cooling(self) -> bool:
        """Return ``True`` if cooling is currently active."""
        return self._cooling_active

    def telemetry(self) -> dict[str, Any]:
        """Return thermal telemetry data."""
        return {
            "temperature_c": round(self._current_temp, 2),
            "cooling_active": self._cooling_active,
        }
