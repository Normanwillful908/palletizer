"""
Communication Interface Module
===============================

The :class:`CommunicationInterface` abstracts telemetry publishing
and remote command reception.  In this reference implementation it
logs messages; extend it to support Ethernet, serial, CAN bus or
MQTT transports as needed.
"""

from __future__ import annotations

import logging
from typing import Any

from ..config import Config


class CommunicationInterface:
    """Publish telemetry and receive remote commands.

    Parameters
    ----------
    config : Config
        System configuration (used to read endpoint settings).
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        self._connected = False
        self._logger = logging.getLogger(self.__class__.__name__)

    def connect(self) -> None:
        """Establish the communication channel.

        In a real deployment this would open a socket, serial port or
        message-broker connection.
        """
        self._connected = True
        self._logger.info("Communication channel connected")

    def disconnect(self) -> None:
        """Close the communication channel."""
        self._connected = False
        self._logger.info("Communication channel disconnected")

    def send_telemetry(self, data: dict[str, Any]) -> None:
        """Publish a telemetry payload.

        Parameters
        ----------
        data : dict
            Key-value telemetry data to publish.
        """
        if not self._connected:
            self._logger.warning("Cannot send telemetry: not connected")
            return
        self._logger.debug("Telemetry: %s", data)

    def receive_command(self) -> dict[str, Any] | None:
        """Poll for an incoming remote command.

        Returns ``None`` if no command is available.
        """
        return None

    @property
    def is_connected(self) -> bool:
        """Return ``True`` if the channel is active."""
        return self._connected
