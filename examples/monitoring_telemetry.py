"""
Monitoring and Telemetry Example
================================

This example shows how to collect and inspect telemetry data from
the palletiser subsystems — battery, thermal, memory and faults.
"""

from __future__ import annotations

import json
import logging

from palletizer_full.config import Config
from palletizer_full.core.fault_detection import FaultDetector
from palletizer_full.core.memory_management import MemoryManager
from palletizer_full.power.battery_management import BatteryManager
from palletizer_full.power.thermal_management import ThermalManager


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    cfg = Config()

    battery = BatteryManager(cfg.battery_capacity_wh, cfg.low_battery_threshold)
    thermal = ThermalManager(cfg.max_temperature_c, cfg.cooling_hysteresis_c)
    memory = MemoryManager(cfg.total_memory_bytes)
    faults = FaultDetector()

    # Simulate a few cycles
    for _i in range(100):
        battery.update(current_draw_w=200.0, dt_s=0.02)
        thermal.update()

    # Simulate a fault
    faults.report_fault("conveyor_jam")

    # Collect telemetry
    telemetry = {
        **battery.telemetry(),
        **thermal.telemetry(),
        "memory_ok": memory.check_health(),
        "active_faults": list(faults.get_active_faults()),
    }

    print(json.dumps(telemetry, indent=2))


if __name__ == "__main__":
    main()
