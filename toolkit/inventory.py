"""
inventory.py - Load and validate the device inventory from YAML.
"""

from pathlib import Path
from typing import List

import yaml

INVENTORY_FILE = Path(__file__).resolve().parent.parent / "inventory" / "devices.yaml"

REQUIRED_FIELDS = ("name", "host", "device_type")


def load_inventory(path: Path = INVENTORY_FILE) -> List[dict]:
    """Load the device inventory and validate required fields.

    Raises ValueError if any device entry is missing a required field.
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}

    devices = data.get("devices", [])
    for device in devices:
        missing = [field for field in REQUIRED_FIELDS if field not in device]
        if missing:
            raise ValueError(f"Device entry missing required fields {missing}: {device}")
    return devices
