"""
Memory Management Module
========================

The :class:`MemoryManager` provides a deterministic allocator to
avoid unpredictable garbage-collection pauses during the control
loop.  Pre-allocating buffers ensures predictable memory usage and
helps detect runaway consumption before it causes failures.
"""

from __future__ import annotations

from typing import Any


class MemoryManager:
    """Deterministic memory allocator for real-time control.

    Parameters
    ----------
    total_bytes : int
        Total amount of memory (bytes) available for allocation.
    """

    def __init__(self, total_bytes: int) -> None:
        self.total_bytes = total_bytes
        self.available_bytes = total_bytes
        self._allocations: dict[Any, int] = {}

    def allocate(self, size: int) -> Any:
        """Reserve a block of memory and return an opaque handle.

        Raises
        ------
        ValueError
            If *size* is not positive.
        MemoryError
            If there is insufficient memory to satisfy the request.
        """
        if size <= 0:
            msg = "Allocation size must be positive"
            raise ValueError(msg)
        if size > self.available_bytes:
            msg = "Insufficient memory available"
            raise MemoryError(msg)
        handle = object()
        self._allocations[handle] = size
        self.available_bytes -= size
        return handle

    def release(self, handle: Any) -> None:
        """Release a previously allocated memory block.

        Double frees or unknown handles are silently ignored.
        """
        size = self._allocations.pop(handle, None)
        if size is not None:
            self.available_bytes += size

    def check_health(self) -> bool:
        """Return ``True`` if at least 10 % of memory remains free."""
        if self.total_bytes == 0:
            return True
        free_ratio = self.available_bytes / self.total_bytes
        return free_ratio >= 0.1
