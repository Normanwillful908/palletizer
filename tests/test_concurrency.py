"""Tests for concurrency primitives."""

from __future__ import annotations

from palletizer_full.core.concurrency_management import ReentrantLock


class TestReentrantLock:
    """Validate reentrant lock behaviour."""

    def test_context_manager(self) -> None:
        lock = ReentrantLock()
        with lock:
            pass  # should not deadlock

    def test_reentrant(self) -> None:
        lock = ReentrantLock()
        with lock, lock:
            pass  # reentrant — should not deadlock

    def test_acquire_release(self) -> None:
        lock = ReentrantLock()
        assert lock.acquire()
        lock.release()
