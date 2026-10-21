"""Lab - one inventory, three formats.

inventory.json, inventory.yaml and inventory.csv hold the same eight servers.
Prove it, then produce a report.

Run  python3 check_formats.py  to test.
"""

import csv
import json
from pathlib import Path

import yaml

HERE = Path(__file__).parent
JSON_FILE = HERE / "inventory.json"
YAML_FILE = HERE / "inventory.yaml"
CSV_FILE = HERE / "inventory.csv"
TRAPS_FILE = HERE / "traps.yaml"

# The CSV has no types - every field is a string. These are the ones that are
# really numbers.
NUMERIC_FIELDS = ("port", "disk_percent_used", "bytes_transferred")


def load_json():
    """CORE - return the list of servers from inventory.json.

    Returns:
        list of dict
    """
    with open(JSON_FILE, encoding="utf-8") as file:
        data = json.load(file)

    return data["servers"]


def load_yaml():
    """CORE - return the list of servers from inventory.yaml.

    Use safe_load, never load.

    Returns:
        list of dict
    """
    # Like your example, safe_load reads the open file into a dictionary.
    with open(YAML_FILE, encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config["servers"]


def load_csv():
    """CORE - return the list of servers from inventory.csv.

    Two things to get right:
      - open with newline="" as well as encoding="utf-8"
      - convert the fields in NUMERIC_FIELDS from str to int, so the rows
        compare equal to the JSON and YAML ones

    Returns:
        list of dict
    """
    servers = []

    with open(CSV_FILE, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for server in reader:
            # CSV reads numbers as strings, so convert these fields.
            for field in NUMERIC_FIELDS:
                server[field] = int(server[field])

            servers.append(server)

    return servers


def all_three_match():
    """CORE - True if all three files hold identical data.

    Returns:
        bool
    """
    json_servers = load_json()
    yaml_servers = load_yaml()
    csv_servers = load_csv()

    return json_servers == yaml_servers == csv_servers


def summarise_by_environment():
    """EXTENSION - one entry per environment.

    Returns:
        list of dicts, sorted by environment name, each with keys:
            "environment", "servers", "bytes"
    """
    summary = {}

    for server in load_yaml():
        environment = server["environment"]

        if environment not in summary:
            summary[environment] = {
                "environment": environment,
                "servers": 0,
                "bytes": 0,
            }

        summary[environment]["servers"] += 1
        summary[environment]["bytes"] += server["bytes_transferred"]

    # Put the environment names in alphabetical order for the report.
    rows = []
    for environment in sorted(summary):
        rows.append(summary[environment])

    return rows


def write_summary_csv(path):
    """EXTENSION - write summarise_by_environment() out as a CSV.

    Header row first, then one row per environment. Use DictWriter, and
    remember newline="".

    Args:
        path: a pathlib.Path to write to
    """
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file, fieldnames=["environment", "servers", "bytes"]
        )
        writer.writeheader()
        writer.writerows(summarise_by_environment())


if __name__ == "__main__":
    print(all_three_match())

    for row in summarise_by_environment():
        print(row)
