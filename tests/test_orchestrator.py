"""Tests for the PalletiserOrchestrator."""

from __future__ import annotations

from palletizer_full.config import Config
from palletizer_full.orchestrator import PalletiserOrchestrator
from tests.conftest import DummyRobot


class TestOrchestrator:
    """Validate orchestrator wiring and basic operation."""

    def test_instantiation(self) -> None:
        cfg = Config()
        robot = DummyRobot()
        orch = PalletiserOrchestrator(cfg, robot)
        assert orch.planner is not None
        assert orch.battery is not None

    def test_add_order(self) -> None:
        cfg = Config()
        robot = DummyRobot()
        orch = PalletiserOrchestrator(cfg, robot)
        orch.pattern_manager.load_pattern("box", [(0.0, 0.0, 0.0)])
        orch.add_order("box", 3)
        assert orch.planner.pending_count == 3

    def test_run_limited_cycles(self) -> None:
        cfg = Config()
        robot = DummyRobot()
        orch = PalletiserOrchestrator(cfg, robot)
        orch.pattern_manager.load_pattern("box", [(0.0, 0.0, 0.0)])
        orch.add_order("box", 1)
        orch.run(cycles=5)  # should complete without error

    def test_collect_metrics(self) -> None:
        cfg = Config()
        robot = DummyRobot()
        orch = PalletiserOrchestrator(cfg, robot)
        metrics = orch._collect_metrics()
        assert "battery_soc" in metrics
        assert "temperature_c" in metrics
        assert "memory_ok" in metrics
