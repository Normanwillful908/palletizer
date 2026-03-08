"""
Mission Planner Module
======================

The :class:`MissionPlanner` breaks down orders into pick/stack
sequences.  It tracks progress, handles errors and recovers from
faults by re-planning or pausing the cell.
"""

from __future__ import annotations

import logging
from collections import deque
from typing import Any

from .pattern_manager import PatternManager


class MissionPlanner:
    """Plan and sequence palletising tasks.

    Parameters
    ----------
    pattern_manager : PatternManager
        Manager providing stacking patterns for each SKU.
    """

    def __init__(self, pattern_manager: PatternManager) -> None:
        self._pattern_manager = pattern_manager
        self._task_queue: deque[dict[str, Any]] = deque()
        self._completed: int = 0
        self._logger = logging.getLogger(self.__class__.__name__)

    def add_order(self, sku: str, quantity: int) -> None:
        """Add a palletising order for *quantity* cases of *sku*.

        The planner looks up the stacking pattern for the SKU and
        generates one task per case.
        """
        try:
            pattern = self._pattern_manager.get_pattern(sku)
        except KeyError:
            self._logger.error("No pattern for SKU '%s'", sku)
            return
        for i in range(quantity):
            pose = pattern[i % len(pattern)]
            self._task_queue.append({
                "sku": sku,
                "index": i,
                "pose": pose,
            })
        self._logger.info("Queued %d tasks for SKU '%s'", quantity, sku)

    def has_next_task(self) -> bool:
        """Return ``True`` if there are pending tasks."""
        return len(self._task_queue) > 0

    def next_task(self) -> dict[str, Any] | None:
        """Pop and return the next task, or ``None`` if empty."""
        if not self._task_queue:
            return None
        task = self._task_queue.popleft()
        self._completed += 1
        return task

    @property
    def completed_count(self) -> int:
        """Number of tasks completed so far."""
        return self._completed

    @property
    def pending_count(self) -> int:
        """Number of tasks remaining in the queue."""
        return len(self._task_queue)
