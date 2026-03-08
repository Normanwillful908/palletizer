"""
Pattern Manager Module
======================

The :class:`PatternManager` generates and stores pallet patterns.
Patterns are lists of ``(x, y, rotation)`` tuples describing where
each case should be placed on a layer.  Patterns can be saved as
JSON and loaded into the planner.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path


class PatternManager:
    """Manage pallet stacking patterns."""

    def __init__(self) -> None:
        self._patterns: dict[str, list[tuple[float, float, float]]] = {}
        self._logger = logging.getLogger(self.__class__.__name__)

    def load_pattern(
        self,
        name: str,
        poses: list[tuple[float, float, float]],
    ) -> None:
        """Register a pattern under *name*."""
        self._patterns[name] = list(poses)
        self._logger.info("Loaded pattern '%s' with %d poses", name, len(poses))

    def get_pattern(self, name: str) -> list[tuple[float, float, float]]:
        """Return the poses for pattern *name*."""
        if name not in self._patterns:
            msg = f"Unknown pattern: {name}"
            raise KeyError(msg)
        return list(self._patterns[name])

    def list_patterns(self) -> list[str]:
        """Return names of all registered patterns."""
        return list(self._patterns.keys())

    def save_to_json(self, path: str | Path) -> None:
        """Persist all patterns to a JSON file."""
        with open(path, "w") as fh:
            json.dump(self._patterns, fh, indent=2)

    def load_from_json(self, path: str | Path) -> None:
        """Load patterns from a JSON file."""
        with open(path) as fh:
            data = json.load(fh)
        for name, poses in data.items():
            self._patterns[name] = [tuple(p) for p in poses]
        self._logger.info("Loaded %d patterns from %s", len(data), path)
