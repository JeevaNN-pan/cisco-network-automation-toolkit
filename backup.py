"""
backup.py - Back up running configuration for every device in the inventory.

Usage:
    python backup.py

Each backup is saved as backups/<device_name>_<timestamp>.cfg. Nothing is
overwritten - every run creates a new timestamped file, so you can diff
between runs to detect configuration drift.
"""

import logging
from datetime import datetime
from pathlib import Path

from toolkit.connection import device_connection
from toolkit.inventory import load_inventory

BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / "backups"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "toolkit.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("toolkit.backup")


def backup_device(device: dict) -> Path:
    """Connect to a device, pull running-config, and save it to disk."""
    with device_connection(device) as conn:
        config = conn.send_command("show running-config")

    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = BACKUP_DIR / f"{device['name']}_{timestamp}.cfg"
    outfile.write_text(config)
    logger.info("Saved backup for %s -> %s", device["name"], outfile)
    return outfile


def main():
    devices = load_inventory()
    if not devices:
        logger.warning("No devices found in inventory.")
        return

    results = {"success": [], "failed": []}
    for device in devices:
        try:
            backup_device(device)
            results["success"].append(device["name"])
        except Exception as exc:  # noqa: BLE001 - log and continue with next device
            logger.error("Backup failed for %s: %s", device["name"], exc)
            results["failed"].append(device["name"])

    logger.info("Backup complete. Success: %s, Failed: %s", results["success"], results["failed"])


if __name__ == "__main__":
    main()
