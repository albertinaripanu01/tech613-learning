"""Pytest examples in one file.

Run from the repository root:
    python -m pytest python/test_pytest_codealong.py -v
"""

import json

import pytest


# 1. Check whether an HTTP status code is healthy.
def is_healthy(status_code):
    """Return True for 200 or 204, and False for other status codes."""
    return status_code in (200, 204)


def test_200_is_healthy():
    assert is_healthy(200) is True


# Parametrisation runs this test once for each pair of inputs.
@pytest.mark.parametrize("status_code, expected", [
    (200, True),
    (204, True),
    (404, False),
    (500, False),
    (301, False),
])

def test_is_healthy(status_code, expected):
    assert is_healthy(status_code) is expected


# 2. Classify disk usage as a percentage.
# This version includes both the WARNING and CRITICAL thresholds.
def classify_disk(used):
    if used >= 90:
        return "CRITICAL"
    if used >= 80:
        return "WARNING"
    return "OK"


def test_disk_at_threshold_is_critical():
    # Arrange: prepare the input.
    disk_used = 90

    # Act: call the function being tested.
    result = classify_disk(disk_used)

    # Assert: check the result.
    assert result == "CRITICAL"


@pytest.mark.parametrize("used, expected", [
    (94, "CRITICAL"),
    (90, "CRITICAL"),
    (89, "WARNING"),
    (80, "WARNING"),
    (79, "OK"),
    (0, "OK"),
])
def test_classify_disk(used, expected):
    assert classify_disk(used) == expected


# 3. Read a JSON inventory file.
def load_inventory(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def test_load_inventory_reads_servers(tmp_path):
    # Pytest supplies tmp_path: a temporary folder for this test.
    config_file = tmp_path / "inventory.json"
    config_file.write_text(
        '{"servers": [{"hostname": "web-01"}]}',
        encoding="utf-8",
    )

    data = load_inventory(config_file)

    assert data["servers"][0]["hostname"] == "web-01"
