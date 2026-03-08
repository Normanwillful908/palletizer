"""
Robot Configuration Parser
==========================

Reads configuration from environment variables and exposes a
strongly-typed, frozen :class:`RobotConfig` dataclass.  This allows
the system to adapt to different factory environments, hardware
configurations and operating modes without changing code.

Boolean values accept ``1``, ``true``, ``t``, ``yes``, ``y`` or
``on`` (case-insensitive) as true; everything else is false.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _env_bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "t", "yes", "y", "on"}


def _env_floats(name: str, default: tuple[float, ...]) -> tuple[float, ...]:
    raw = os.getenv(name)
    if not raw:
        return default
    out: list[float] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            out.append(float(part))
        except ValueError:
            msg = f"Invalid float in {name}: {part}"
            raise ValueError(msg) from None
    return tuple(out)


def _env_csv(name: str, default: tuple[str, ...]) -> tuple[str, ...]:
    raw = os.getenv(name)
    if not raw:
        return default
    return tuple(s.strip() for s in raw.split(",") if s.strip())


# ---------------------------------------------------------------------------
# RobotConfig
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RobotConfig:
    """Configuration for the palletiser control stack.

    Fields correspond to environment variables prefixed with
    ``PALLETIZER_``.
    """

    robot_environment: str
    operation_mode: str
    simulator_enabled: bool
    joint_ids: tuple[str, ...]
    actuator_types: tuple[str, ...]
    max_velocity_per_joint: tuple[float, ...]
    max_torque_per_joint: tuple[float, ...]
    min_safety_margin: float
    safety_thresholds: tuple[float, ...]
    control_frequency_hz: float
    communication_endpoint: str | None

    def __init__(self) -> None:
        object.__setattr__(self, "robot_environment", _env("PALLETIZER_ENV", "FACTORY"))
        object.__setattr__(self, "operation_mode", _env("PALLETIZER_MODE", "PRODUCTION"))
        object.__setattr__(self, "simulator_enabled", _env_bool("PALLETIZER_SIM", False))
        object.__setattr__(
            self,
            "joint_ids",
            _env_csv("PALLETIZER_JOINT_IDS", ("j0", "j1", "j2", "j3", "j4", "j5")),
        )
        object.__setattr__(
            self,
            "actuator_types",
            _env_csv("PALLETIZER_ACTUATORS", ("REVOLUTE",) * 6),
        )
        object.__setattr__(
            self,
            "max_velocity_per_joint",
            _env_floats("PALLETIZER_MAX_VEL", (1.0,) * 6),
        )
        object.__setattr__(
            self,
            "max_torque_per_joint",
            _env_floats("PALLETIZER_MAX_TORQUE", (100.0,) * 6),
        )
        object.__setattr__(
            self,
            "min_safety_margin",
            float(os.getenv("PALLETIZER_SAFETY_MARGIN", "0.4")),
        )
        object.__setattr__(
            self,
            "safety_thresholds",
            _env_floats("PALLETIZER_SAFETY_THRESHOLDS", ()),
        )
        object.__setattr__(
            self,
            "control_frequency_hz",
            float(os.getenv("PALLETIZER_FREQ", "50.0")),
        )
        object.__setattr__(
            self,
            "communication_endpoint",
            os.getenv("PALLETIZER_COMM_ENDPOINT"),
        )
