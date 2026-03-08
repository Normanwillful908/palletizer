"""Tests for the HazardManager."""

from __future__ import annotations

from palletizer_full.config import Config
from palletizer_full.core.hazard_manager import HazardManager


class TestHazardManager:
    """Validate hazard detection and safety decisions."""

    def test_safe_when_no_hazards(self, config: Config) -> None:
        hm = HazardManager(config)
        hm.update({})
        assert hm.is_safe()

    def test_proximity_hazard(self, config: Config) -> None:
        hm = HazardManager(config)
        hm.update({"proximity": 0.1})
        assert not hm.is_safe()
        hazards = hm.current_hazards()
        assert "proximity" in hazards

    def test_proximity_safe(self, config: Config) -> None:
        hm = HazardManager(config)
        hm.update({"proximity": 1.0})
        assert hm.is_safe()

    def test_fault_hazard(self, config: Config) -> None:
        hm = HazardManager(config)
        hm.update({"faults": ["overheat"]})
        assert not hm.is_safe()
        hazards = hm.current_hazards()
        assert "fault:overheat" in hazards

    def test_multiple_faults(self, config: Config) -> None:
        hm = HazardManager(config)
        hm.update({"faults": ["overheat", "gripper_fail"]})
        hazards = hm.current_hazards()
        assert len(hazards) == 2

    def test_invalid_signals(self, config: Config) -> None:
        hm = HazardManager(config)
        hm.update("not a dict")  # type: ignore[arg-type]
        assert hm.is_safe()

    def test_numeric_hazard_with_threshold(self) -> None:
        cfg = Config()
        object.__setattr__(cfg, "safety_thresholds", (5.0,))
        hm = HazardManager(cfg)
        hm.update({"high_voltage": 10.0})
        assert not hm.is_safe()

    def test_numeric_hazard_below_threshold(self) -> None:
        cfg = Config()
        object.__setattr__(cfg, "safety_thresholds", (5.0,))
        hm = HazardManager(cfg)
        hm.update({"high_voltage": 3.0})
        assert hm.is_safe()
