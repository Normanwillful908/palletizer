"""
Concurrency Management Module
==============================

Provides thread-safe primitives for coordinating access to shared
resources in a multi-threaded control loop.  The
:class:`ReentrantLock` wraps Python's ``threading.RLock`` and can be
used as a context manager.
"""

from __future__ import annotations

import threading


class ReentrantLock:
    """A reentrant lock that can be used as a context manager.

    This thin wrapper around :class:`threading.RLock` provides a
    consistent API for the palletiser control stack.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()

    def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
        """Acquire the lock."""
        return self._lock.acquire(blocking=blocking, timeout=timeout)

    def release(self) -> None:
        """Release the lock."""
        self._lock.release()

    def __enter__(self) -> ReentrantLock:
        self._lock.acquire()
        return self

    def __exit__(self, *args: object) -> None:
        self._lock.release()
