"""
Environment Adapter Module
===========================

Provides helpers to adapt system behaviour to different factory
environments.  The :class:`EnvironmentAdapter` reads the current
environment profile and applies adjustments to safety margins,
cycle rates and other parameters.
"""

from __future__ import annotations

import logging
from typing import ClassVar

from ..config import Config


class EnvironmentAdapter:
    """Adapt system parameters to the deployment environment.

    Parameters
    ----------
    config : Config
        System configuration to adjust.
    environment : str
        Environment identifier (e.g. ``"FACTORY"``, ``"WAREHOUSE"``).
    """

    PROFILES: ClassVar[dict[str, dict[str, float]]] = {
        "FACTORY": {"safety_margin_m": 0.4, "cycle_hz": 50.0},
        "WAREHOUSE": {"safety_margin_m": 0.6, "cycle_hz": 30.0},
        "LAB": {"safety_margin_m": 0.2, "cycle_hz": 100.0},
    }

    def __init__(self, config: Config, environment: str = "FACTORY") -> None:
        self._config = config
        self._environment = environment.upper()
        self._logger = logging.getLogger(self.__class__.__name__)

    def apply(self) -> Config:
        """Apply environment-specific overrides and return the config."""
        profile = self.PROFILES.get(self._environment, {})
        for key, value in profile.items():
            if hasattr(self._config, key):
                object.__setattr__(self._config, key, value)
                self._logger.info(
                    "Environment %s: set %s = %s",
                    self._environment,
                    key,
                    value,
                )
        return self._config
