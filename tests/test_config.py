"""Tests for the Config module."""

from __future__ import annotations

from palletizer_full.config import Config


class TestConfig:
    """Validate Config defaults and cycle_time calculation."""

    def test_default_cycle_hz(self) -> None:
        cfg = Config()
        assert cfg.cycle_hz == 50.0

    def test_cycle_time(self) -> None:
        cfg = Config()
        assert abs(cfg.cycle_time() - 0.02) < 1e-6

    def test_safety_margin_default(self) -> None:
        cfg = Config()
        assert cfg.safety_margin_m == 0.4

    def test_battery_capacity_default(self) -> None:
        cfg = Config()
        assert cfg.battery_capacity_wh == 1000.0

    def test_max_temperature_default(self) -> None:
        cfg = Config()
        assert cfg.max_temperature_c == 70.0
