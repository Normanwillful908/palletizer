"""Tests for the FaultDetector."""

from __future__ import annotations

from palletizer_full.core.fault_detection import FaultDetector


class TestFaultDetector:
    """Validate fault registration, clearing and querying."""

    def test_report_and_query(self) -> None:
        fd = FaultDetector()
        fd.report_fault("overheat")
        assert "overheat" in fd.get_active_faults()

    def test_clear_fault(self) -> None:
        fd = FaultDetector()
        fd.report_fault("overheat")
        fd.clear_fault("overheat")
        assert "overheat" not in fd.get_active_faults()

    def test_clear_all(self) -> None:
        fd = FaultDetector()
        fd.report_fault("a")
        fd.report_fault("b")
        fd.clear_all()
        assert len(list(fd.get_active_faults())) == 0

    def test_ignore_empty_string(self) -> None:
        fd = FaultDetector()
        fd.report_fault("")
        assert len(list(fd.get_active_faults())) == 0

    def test_clear_nonexistent(self) -> None:
        fd = FaultDetector()
        fd.clear_fault("does_not_exist")  # should not raise
