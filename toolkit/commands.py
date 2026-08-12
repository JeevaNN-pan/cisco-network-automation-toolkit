"""
commands.py - Run show commands against inventory devices and return
lightly parsed results (interface status, VLANs, routing table).

This intentionally uses simple line parsing rather than a heavyweight
parser (e.g. Genie/pyATS) to keep the toolkit dependency-light and easy to
read for portfolio/learning purposes. See README Limitations for the
parsing caveats this implies.
"""

import logging

from toolkit.connection import device_connection

logger = logging.getLogger("toolkit.commands")


def run_show_command(device: dict, command: str) -> str:
    """Run a single show command on a device and return raw text output."""
    with device_connection(device) as conn:
        return conn.send_command(command)


def get_interface_status(device: dict):
    """Parse 'show ip interface brief' into a list of dicts."""
    output = run_show_command(device, "show ip interface brief")
    interfaces = []
    for line in output.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 6:
            interfaces.append(
                {
                    "interface": parts[0],
                    "ip_address": parts[1],
                    "status": parts[4],
                    "protocol": parts[5],
                }
            )
    return interfaces


def get_vlans(device: dict):
    """Parse 'show vlan brief' into a list of dicts."""
    output = run_show_command(device, "show vlan brief")
    vlans = []
    for line in output.splitlines():
        parts = line.split()
        if parts and parts[0].isdigit():
            vlans.append({"vlan_id": parts[0], "name": parts[1], "status": parts[2]})
    return vlans


def get_routing_table(device: dict) -> str:
    """Return the raw 'show ip route' output.

    Routing table formats vary too much across topologies/protocols to
    usefully parse generically here, so this returns raw text for the
    caller (or a human) to inspect.
    """
    return run_show_command(device, "show ip route")
