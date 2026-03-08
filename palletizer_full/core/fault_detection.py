"""
Fault Detection Module
======================

The :class:`FaultDetector` monitors actuators, sensors and control
loops for anomalies.  It maintains a set of active fault identifiers
and exposes interfaces to register, clear and query them.  Detected
faults are forwarded to the hazard manager so they can be treated
uniformly with environmental hazards.
"""

from __future__ import annotations

from collections.abc import Iterable


class FaultDetector:
    """Track and manage system faults."""

    def __init__(self) -> None:
        self._active_faults: set[str] = set()

    def report_fault(self, fault: str) -> None:
        """Register a new fault identifier."""
        if isinstance(fault, str) and fault:
            self._active_faults.add(fault)

    def clear_fault(self, fault: str) -> None:
        """Clear a previously reported fault."""
        self._active_faults.discard(fault)

    def clear_all(self) -> None:
        """Clear all active faults."""
        self._active_faults.clear()

    def get_active_faults(self) -> Iterable[str]:
        """Return an iterable of currently active faults."""
        return tuple(self._active_faults)
