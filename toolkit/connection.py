"""
connection.py - Netmiko connection helper for Cisco IOS devices.

Credentials are never hard-coded. Set them via environment variables:
    NET_USERNAME, NET_PASSWORD, NET_SECRET (enable password, optional)

See .env.example for the expected format if you use a .env loader such as
python-dotenv (not required - exporting the variables in your shell works
just as well).
"""

import logging
import os
from contextlib import contextmanager

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

logger = logging.getLogger("toolkit.connection")


class CredentialsError(RuntimeError):
    """Raised when required credentials are missing from the environment."""


def _get_credentials():
    username = os.environ.get("NET_USERNAME")
    password = os.environ.get("NET_PASSWORD")
    secret = os.environ.get("NET_SECRET", "")

    if not username or not password:
        raise CredentialsError(
            "NET_USERNAME and NET_PASSWORD environment variables are required. "
            "See .env.example."
        )
    return username, password, secret


@contextmanager
def device_connection(device: dict):
    """Open a Netmiko connection to a single inventory device.

    device: dict with at least 'host' and 'device_type' (e.g. 'cisco_ios').
    Yields a connected Netmiko handler and always disconnects afterwards.
    """
    username, password, secret = _get_credentials()

    params = {
        "device_type": device.get("device_type", "cisco_ios"),
        "host": device["host"],
        "username": username,
        "password": password,
        "secret": secret,
        "timeout": device.get("timeout", 10),
    }

    connection = None
    try:
        logger.info("Connecting to %s (%s)", device.get("name", device["host"]), device["host"])
        connection = ConnectHandler(**params)
        if secret:
            connection.enable()
        yield connection
    except NetmikoAuthenticationException as exc:
        logger.error("Authentication failed for %s: %s", device.get("name"), exc)
        raise
    except NetmikoTimeoutException as exc:
        logger.error("Connection to %s timed out: %s", device.get("name"), exc)
        raise
    finally:
        if connection:
            connection.disconnect()
            logger.info("Disconnected from %s", device.get("name", device["host"]))
