"""Tests for the MemoryManager."""

from __future__ import annotations

import pytest

from palletizer_full.core.memory_management import MemoryManager


class TestMemoryManager:
    """Validate allocation, release and health checks."""

    def test_allocate_and_release(self) -> None:
        mm = MemoryManager(1024)
        handle = mm.allocate(512)
        assert mm.available_bytes == 512
        mm.release(handle)
        assert mm.available_bytes == 1024

    def test_allocate_too_large(self) -> None:
        mm = MemoryManager(100)
        with pytest.raises(MemoryError):
            mm.allocate(200)

    def test_allocate_zero(self) -> None:
        mm = MemoryManager(100)
        with pytest.raises(ValueError):
            mm.allocate(0)

    def test_health_check_healthy(self) -> None:
        mm = MemoryManager(1000)
        mm.allocate(800)
        assert mm.check_health()

    def test_health_check_unhealthy(self) -> None:
        mm = MemoryManager(1000)
        mm.allocate(950)
        assert not mm.check_health()

    def test_double_release_ignored(self) -> None:
        mm = MemoryManager(1024)
        handle = mm.allocate(100)
        mm.release(handle)
        mm.release(handle)  # should not raise
        assert mm.available_bytes == 1024
