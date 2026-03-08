"""
Hazard Manager Module
=====================

The :class:`HazardManager` monitors environmental signals and
internal states to detect potentially dangerous conditions.  It
provides a unified API for querying whether the palletiser can
continue operating safely and for obtaining structured alerts about
detected hazards.

Typical hazards include proximity to humans or other machines,
high voltage, gas or dust levels, overheated actuators and
electrical faults.
"""

from __future__ import annotations

import logging
from typing import Any

from ..config import Config


class HazardManager:
    """Monitor environmental and internal hazards.

    Parameters
    ----------
    config : Config
        System configuration including safety thresholds.
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._hazards: dict[str, dict[str, Any]] = {}
        self._logger = logging.getLogger(self.__class__.__name__)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update(self, signals: dict[str, Any]) -> None:
        """Update hazard state based on new sensor signals.

        Supported keys in *signals*:

        * ``proximity`` — distance to nearest obstacle (metres).
        * ``high_voltage``, ``gas``, ``radiation`` — scalar values
          compared against ``config.safety_thresholds[0..2]``.
        * ``faults`` — iterable of fault identifier strings.
        """
        self._hazards.clear()
        if not isinstance(signals, dict):
            return

        def _threshold(idx: int, default: float = 1.0) -> float:
            try:
                return float(self._config.safety_thresholds[idx])
            except Exception:
                return default

        # Proximity
        prox = signals.get("proximity")
        if prox is not None:
            try:
                distance = float(prox)
                if distance < self._config.safety_margin_m:
                    self._hazards["proximity"] = {
                        "value": distance,
                        "threshold": self._config.safety_margin_m,
                        "message": (
                            f"Object within {distance:.2f} m "
                            f"(min {self._config.safety_margin_m} m)"
                        ),
                        "risk_level": "high",
                    }
            except Exception:
                pass

        # Numeric hazards
        for idx, name in enumerate(["high_voltage", "gas", "radiation"]):
            val = signals.get(name)
            if val is None:
                continue
            try:
                level = float(val)
            except Exception:
                continue
            thresh = _threshold(idx)
            if level > thresh:
                self._hazards[name] = {
                    "value": level,
                    "threshold": thresh,
                    "message": (
                        f"{name.replace('_', ' ').title()} level "
                        f"{level:.2f} exceeds {thresh:.2f}"
                    ),
                    "risk_level": "high",
                }

        # Fault hazards
        faults = signals.get("faults")
        if faults:
            if isinstance(faults, str):
                faults_iter: list[str] = [faults]
            elif isinstance(faults, (list, tuple, set)):
                faults_iter = [str(f) for f in faults]
            else:
                faults_iter = []
            for fault_name in faults_iter:
                self._hazards[f"fault:{fault_name}"] = {
                    "value": True,
                    "threshold": True,
                    "message": f"Fault detected: {fault_name}",
                    "risk_level": "high",
                }

    def is_safe(self) -> bool:
        """Return ``True`` if the palletiser may continue operating."""
        if not self._hazards:
            return True
        return all(
            str(info.get("risk_level", "high")).lower() != "high"
            for info in self._hazards.values()
        )

    def current_hazards(self) -> dict[str, dict[str, Any]]:
        """Return a dictionary of the currently detected hazards."""
        return dict(self._hazards)
