"""
Execution Stack Module
======================

The :class:`ExecutionStack` manages the deterministic control loop.
It sequences sensor polling, planning, control and actuation at a
fixed cycle rate, invokes health checks and publishes telemetry.
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from typing import Any

from ..config import Config


class ExecutionStack:
    """Manage the main control loop.

    Parameters
    ----------
    config : Config
        Global configuration for the system.
    on_cycle : Callable[[float], None]
        Callback invoked every cycle with the elapsed time.
    on_health_check : Callable[[], dict[str, Any]]
        Callback invoked each cycle to collect telemetry.
    """

    def __init__(
        self,
        config: Config,
        on_cycle: Callable[[float], None],
        on_health_check: Callable[[], dict[str, Any]],
    ) -> None:
        self._config = config
        self._on_cycle = on_cycle
        self._on_health_check = on_health_check
        self._logger = logging.getLogger(self.__class__.__name__)

    def run(self, cycles: int | None = None) -> None:
        """Run the control loop.

        Parameters
        ----------
        cycles : int | None
            Number of cycles to run.  If ``None``, runs indefinitely.
        """
        cycle_time = self._config.cycle_time()
        next_time = time.monotonic()
        cycle_count = 0
        while cycles is None or cycle_count < cycles:
            now = time.monotonic()
            dt = now - next_time + cycle_time
            try:
                self._on_cycle(dt)
            except Exception:
                self._logger.exception("Error in control cycle")
            try:
                self._on_health_check()
            except Exception:
                self._logger.exception("Error collecting health metrics")
            next_time += cycle_time
            sleep_time = next_time - time.monotonic()
            if sleep_time > 0:
                time.sleep(sleep_time)
            cycle_count += 1
