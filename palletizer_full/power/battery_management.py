"""
Battery Management Module
=========================

The :class:`BatteryManager` monitors state-of-charge and available
energy.  It uses LiFePO4 battery models by default, as these cells
offer high energy density, long cycle life and excellent safety
characteristics.
"""

from __future__ import annotations

import logging
from typing import Any


class BatteryManager:
    """Monitor battery state-of-charge and energy.

    Parameters
    ----------
    capacity_wh : float
        Total battery capacity in watt-hours.
    low_threshold : float
        Fractional charge level (0-1) below which the battery is
        considered low.
    """

    def __init__(self, capacity_wh: float, low_threshold: float = 0.2) -> None:
        self._capacity_wh = capacity_wh
        self._remaining_wh = capacity_wh
        self._low_threshold = low_threshold
        self._logger = logging.getLogger(self.__class__.__name__)

    def update(self, current_draw_w: float, dt_s: float = 0.02) -> None:
        """Update the remaining energy based on current draw.

        Parameters
        ----------
        current_draw_w : float
            Instantaneous power draw in watts.
        dt_s : float
            Time step in seconds (defaults to 50 Hz cycle).
        """
        consumed = current_draw_w * (dt_s / 3600.0)
        self._remaining_wh = max(0.0, self._remaining_wh - consumed)

    @property
    def soc(self) -> float:
        """State of charge as a fraction (0-1)."""
        if self._capacity_wh <= 0:
            return 0.0
        return self._remaining_wh / self._capacity_wh

    def is_low(self) -> bool:
        """Return ``True`` if the battery is below the low threshold."""
        return self.soc < self._low_threshold

    def telemetry(self) -> dict[str, Any]:
        """Return battery telemetry data."""
        return {
            "battery_soc": round(self.soc, 4),
            "battery_remaining_wh": round(self._remaining_wh, 2),
            "battery_low": self.is_low(),
        }
