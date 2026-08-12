"""
show_inventory_report.py - Connect to every device in the inventory and
print a quick interface/VLAN summary using tabulate.

Usage:
    python show_inventory_report.py
"""

import logging

from tabulate import tabulate

from toolkit.commands import get_interface_status, get_vlans
from toolkit.inventory import load_inventory

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("toolkit.report")


def main():
    devices = load_inventory()
    if not devices:
        logger.warning("No devices found in inventory.")
        return

    for device in devices:
        print(f"\n=== {device['name']} ({device['host']}) ===")

        try:
            interfaces = get_interface_status(device)
            print(tabulate(interfaces, headers="keys", tablefmt="github"))
        except Exception as exc:  # noqa: BLE001 - report and continue with next device
            logger.error("Failed to get interfaces for %s: %s", device["name"], exc)

        try:
            vlans = get_vlans(device)
            if vlans:
                print(tabulate(vlans, headers="keys", tablefmt="github"))
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to get VLANs for %s: %s", device["name"], exc)


if __name__ == "__main__":
    main()
