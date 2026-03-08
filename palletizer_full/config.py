"""
High-level configuration for the palletiser control system.

This module defines a :class:`Config` dataclass that centralises
parameters for the control loop, power management and safety.  Values
can be overridden via environment variables so that the same codebase
adapts to different factory environments without code changes.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Environment-variable helpers
# ---------------------------------------------------------------------------

def _env_float(name: str, default: float) -> float:
    """Parse a float from an environment variable or return *default*."""
    try:
        raw = os.getenv(name)
        return float(raw) if raw not in (None, "") else default
    except Exception:
        return default


def _env_int(name: str, default: int) -> int:
    """Parse an int from an environment variable or return *default*."""
    try:
        raw = os.getenv(name)
        return int(raw) if raw not in (None, "") else default
    except Exception:
        return default


def _env_bool(name: str, default: bool = False) -> bool:
    """Parse a boolean from an environment variable."""
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


# ---------------------------------------------------------------------------
# Config dataclass
# ---------------------------------------------------------------------------

@dataclass
class Config:
    """Top-level configuration for the palletiser.

    Parameters can be overridden via environment variables.  The
    defaults here are suitable for a typical single-cell palletiser
    using a 50 Hz control loop.
    """

    cycle_hz: float = field(
        default_factory=lambda: _env_float("CYCLE_HZ", 50.0),
    )
    """Control loop frequency in Hertz."""

    battery_capacity_wh: float = field(
        default_factory=lambda: _env_float("BATTERY_CAPACITY_WH", 1000.0),
    )
    """Total energy capacity of the power system in watt-hours."""

    low_battery_threshold: float = field(
        default_factory=lambda: _env_float("LOW_BATTERY_THRESHOLD", 0.2),
    )
    """Fractional charge level below which the system should initiate
    orderly shutdown or trigger a recharge.  Range: 0-1."""

    max_temperature_c: float = field(
        default_factory=lambda: _env_float("MAX_TEMPERATURE_C", 70.0),
    )
    """Maximum safe temperature (deg C) for motors and electronics."""

    cooling_hysteresis_c: float = field(
        default_factory=lambda: _env_float("COOLING_HYSTERESIS_C", 10.0),
    )
    """Temperature difference (deg C) between activating and
    deactivating cooling."""

    total_memory_bytes: int = field(
        default_factory=lambda: _env_int("TOTAL_MEMORY_BYTES", 16 * 1024 * 1024),
    )
    """Amount of memory (bytes) reserved for deterministic buffers."""

    safety_margin_m: float = field(
        default_factory=lambda: _env_float("SAFETY_MARGIN_M", 0.4),
    )
    """Minimum allowable distance (metres) to human operators or
    obstacles."""

    safety_thresholds: tuple[float, ...] = field(
        default_factory=lambda: tuple(
            float(x)
            for x in os.getenv("SAFETY_THRESHOLDS", "").split(",")
            if x.strip()
        ),
    )
    """Generic thresholds for hazards (e.g. gas, voltage)."""

    power_budget_w: float = field(
        default_factory=lambda: _env_float("POWER_BUDGET_W", 2000.0),
    )
    """Power budget (watts) allocated for the cell."""

    enable_monitoring_ui: bool = field(
        default_factory=lambda: _env_bool("ENABLE_MONITORING_UI", True),
    )
    """Whether to launch a simple monitoring server."""

    monitor_port: int = field(
        default_factory=lambda: _env_int("MONITOR_PORT", 8080),
    )
    """Port number for the monitoring UI, if enabled."""

    def cycle_time(self) -> float:
        """Return the period of the control loop in seconds."""
        return 1.0 / max(self.cycle_hz, 1e-3)
