"""Tests for BatteryManager and ThermalManager."""

from __future__ import annotations

from palletizer_full.power.battery_management import BatteryManager
from palletizer_full.power.thermal_management import ThermalManager


class TestBatteryManager:
    """Validate battery state-of-charge tracking."""

    def test_initial_soc(self) -> None:
        bm = BatteryManager(1000.0)
        assert bm.soc == 1.0

    def test_discharge(self) -> None:
        bm = BatteryManager(1000.0)
        bm.update(current_draw_w=1000.0, dt_s=3600.0)
        assert abs(bm.soc) < 0.01

    def test_is_low(self) -> None:
        bm = BatteryManager(1000.0, low_threshold=0.5)
        bm.update(current_draw_w=1000.0, dt_s=1801.0)
        assert bm.is_low()

    def test_telemetry(self) -> None:
        bm = BatteryManager(1000.0)
        t = bm.telemetry()
        assert "battery_soc" in t
        assert "battery_remaining_wh" in t


class TestThermalManager:
    """Validate thermal monitoring and cooling hysteresis."""

    def test_initial_state(self) -> None:
        tm = ThermalManager(max_temp_c=70.0)
        assert not tm.is_cooling

    def test_overheat_triggers_cooling(self) -> None:
        tm = ThermalManager(max_temp_c=70.0)
        tm.update(temperature_c=75.0)
        assert tm.is_cooling

    def test_hysteresis(self) -> None:
        tm = ThermalManager(max_temp_c=70.0, hysteresis_c=10.0)
        tm.update(temperature_c=75.0)
        assert tm.is_cooling
        tm.update(temperature_c=65.0)
        assert tm.is_cooling  # still above 60 threshold
        tm.update(temperature_c=55.0)
        assert not tm.is_cooling

    def test_telemetry(self) -> None:
        tm = ThermalManager()
        t = tm.telemetry()
        assert "temperature_c" in t
        assert "cooling_active" in t
