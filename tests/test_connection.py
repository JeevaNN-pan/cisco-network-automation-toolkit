"""
Unit tests for toolkit.connection - Netmiko is mocked, no real devices or
network access are used.
"""

from unittest.mock import MagicMock, patch

import pytest

from toolkit.connection import CredentialsError, device_connection


def test_missing_credentials_raises(monkeypatch):
    monkeypatch.delenv("NET_USERNAME", raising=False)
    monkeypatch.delenv("NET_PASSWORD", raising=False)
    with pytest.raises(CredentialsError):
        with device_connection({"name": "r1", "host": "10.0.0.1"}):
            pass


def test_successful_connection(monkeypatch):
    monkeypatch.setenv("NET_USERNAME", "admin")
    monkeypatch.setenv("NET_PASSWORD", "secret")
    with patch("toolkit.connection.ConnectHandler") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        with device_connection(
            {"name": "r1", "host": "10.0.0.1", "device_type": "cisco_ios"}
        ) as conn:
            assert conn is mock_conn
        mock_conn.disconnect.assert_called_once()
