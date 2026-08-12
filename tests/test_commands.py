"""
Unit tests for toolkit.commands parsing logic - no network access
required, run_show_command is mocked.
"""

from unittest.mock import patch

from toolkit.commands import get_interface_status, get_vlans

SAMPLE_IP_INT_BRIEF = (
    "Interface                  IP-Address      OK? Method Status                Protocol\n"
    "GigabitEthernet0/0          192.168.1.1     YES manual up                    up\n"
    "GigabitEthernet0/1          unassigned      YES unset  administratively      down\n"
)

SAMPLE_VLAN_BRIEF = (
    "VLAN Name                             Status    Ports\n"
    "---- -------------------------------- --------- -------------------------------\n"
    "1    default                          active    Gi0/2, Gi0/3\n"
    "10   USERS                            active    Gi0/4\n"
)


def test_get_interface_status():
    with patch("toolkit.commands.run_show_command", return_value=SAMPLE_IP_INT_BRIEF):
        result = get_interface_status({"name": "r1", "host": "10.0.0.1"})
    assert result[0]["interface"] == "GigabitEthernet0/0"
    assert result[0]["status"] == "up"
    assert result[1]["interface"] == "GigabitEthernet0/1"


def test_get_vlans():
    with patch("toolkit.commands.run_show_command", return_value=SAMPLE_VLAN_BRIEF):
        result = get_vlans({"name": "r1", "host": "10.0.0.1"})
    assert result[0]["vlan_id"] == "1"
    assert result[0]["name"] == "default"
    assert result[1]["vlan_id"] == "10"
