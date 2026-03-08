"""Tests for the CommunicationInterface."""

from __future__ import annotations

from palletizer_full.config import Config
from palletizer_full.core.communication import CommunicationInterface


class TestCommunicationInterface:
    """Validate connection state and telemetry publishing."""

    def test_connect_disconnect(self, config: Config) -> None:
        ci = CommunicationInterface(config)
        assert not ci.is_connected
        ci.connect()
        assert ci.is_connected
        ci.disconnect()
        assert not ci.is_connected

    def test_send_telemetry_when_connected(self, config: Config) -> None:
        ci = CommunicationInterface(config)
        ci.connect()
        ci.send_telemetry({"test": 1})  # should not raise

    def test_send_telemetry_when_disconnected(self, config: Config) -> None:
        ci = CommunicationInterface(config)
        ci.send_telemetry({"test": 1})  # should log warning, not raise

    def test_receive_command_returns_none(self, config: Config) -> None:
        ci = CommunicationInterface(config)
        assert ci.receive_command() is None
