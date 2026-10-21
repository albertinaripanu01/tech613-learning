"""Lab - summarise a JSON server inventory.

Two files are in this folder:

    inventory.json          a good copy
    inventory_broken.json   the same data with three deliberate defects

Both are valid JSON. The defects are in the *records*, not the syntax - which is
exactly how real data arrives. A file that parses is not a file you can trust.

Run  python3 check_inventory_report.py  to test.
"""

import json
from pathlib import Path

HERE = Path(__file__).parent
GOOD = HERE / "inventory.json"
BROKEN = HERE / "inventory_broken.json"

# A record must have all of these to be usable.
REQUIRED = ("hostname", "environment", "port", "bytes_transferred")


def load_inventory(path):
    """CORE - load a JSON file and return the whole object.

    Use a context manager and an explicit encoding.

    Args:
        path: a pathlib.Path

    Returns:
        dict
    """
    # TODO
    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"Inventory file not found: {path}")
        raise

    except PermissionError:
        print(f"You do not have permission to read: {path}")
        raise

    except json.JSONDecodeError as error:
        print(f"Inventory file contains invalid JSON: {error}")
        raise

    return data


def summarise(path):
    """CORE - summarise the inventory at `path`.

    Returns:
        dict with exactly these keys:
            "total"       how many server records there are
            "production"  how many are in the production environment
            "bytes"       the sum of bytes_transferred
    """
    # TODO
    data = load_inventory(path)
    summary = {"total": 0, "production": 0, "bytes": 0}
    try:
        for server in data["servers"]:
            summary["total"] += 1
            if server["environment"] == "production":
                summary["production"] += 1
            summary["bytes"] += server["bytes_transferred"]

    except KeyError as error:
        print(f"Inventory is missing a required key: {error}")
        raise
    except TypeError as error:
        print(f"Inventory contains an incorrect data type: {error}")
        raise
    return summary


def summarise_safely(path):
    """EXTENSION - summarise, skipping records that cannot be used.

    A record is unusable if it is missing any key in REQUIRED, or if its port
    is not an integer. Do not crash on either.

    Returns:
        tuple of (summary, skipped) where
            summary  is the same dict shape as summarise(), counting only the
                     usable records
            skipped  is a list of (hostname, reason) tuples
    """
    # TODO
    return ({"total": 0, "production": 0, "bytes": 0}, [])


def write_report(path, summary, skipped):
    """STRETCH - write the summary out as JSON.

    Include a generated_on timestamp. datetime is not taught until Day 4, so
    this is enough:

        from datetime import datetime, timezone
        datetime.now(timezone.utc).isoformat()

    Then load the file back and confirm it matches what you wrote. A round trip
    is the cheapest test there is.

    Args:
        path: a pathlib.Path to write to
        summary: the dict from summarise_safely
        skipped: the list from summarise_safely
    """
    # TODO
    pass


if __name__ == "__main__":
    print("good file:  ", summarise(GOOD))

    summary, skipped = summarise_safely(BROKEN)
    print("broken file:", summary)
    for hostname, reason in skipped:
        print(f"  skipped {hostname}: {reason}")
