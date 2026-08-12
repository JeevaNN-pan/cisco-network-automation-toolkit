"""
Unit tests for toolkit.inventory - no network access required.
"""

import textwrap

import pytest

from toolkit.inventory import load_inventory


def test_load_inventory_valid(tmp_path):
    inventory_file = tmp_path / "devices.yaml"
    inventory_file.write_text(
        textwrap.dedent(
            """
            devices:
              - name: r1
                host: 10.0.0.1
                device_type: cisco_ios
            """
        )
    )
    devices = load_inventory(inventory_file)
    assert devices == [{"name": "r1", "host": "10.0.0.1", "device_type": "cisco_ios"}]


def test_load_inventory_missing_field(tmp_path):
    inventory_file = tmp_path / "devices.yaml"
    inventory_file.write_text(
        textwrap.dedent(
            """
            devices:
              - name: r1
                host: 10.0.0.1
            """
        )
    )
    with pytest.raises(ValueError):
        load_inventory(inventory_file)


def test_load_inventory_empty_file(tmp_path):
    inventory_file = tmp_path / "devices.yaml"
    inventory_file.write_text("")
    assert load_inventory(inventory_file) == []
