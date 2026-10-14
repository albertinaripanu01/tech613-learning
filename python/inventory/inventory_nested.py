"""STRETCH - the same data, grouped by environment instead of a flat list.

This is a dictionary whose values are lists of dictionaries. Getting a value out
of it means going three levels deep, which is exactly what your Friday config
file will need.

Run  python3 check_inventory.py  to test.
"""

FLEET = {
    "site": "eu-west",
    "environments": {
        "production": [
            {"hostname": "web-01", "bytes_transferred": 8419203},
            {"hostname": "web-02", "bytes_transferred": 7733910},
            {"hostname": "api-01", "bytes_transferred": 15220477},
            {"hostname": "api-02", "bytes_transferred": 14098320},
            {"hostname": "db-01", "bytes_transferred": 2044118},
        ],
        "staging": [
            {"hostname": "web-01-stg", "bytes_transferred": 402117},
            {"hostname": "api-01-stg", "bytes_transferred": 0},
        ],
        "tooling": [
            {"hostname": "build-01", "bytes_transferred": 630885},
        ],
    },
}


def bytes_per_environment():
    """STRETCH - return a dict of environment name to total bytes.

    Expected shape - one key per environment, each value the sum of
    bytes_transferred for the servers in it:

        {"production": <int>, "staging": <int>, "tooling": <int>}

    Returns:
        dict
    """
    # TODO: loop over the environments, and over the servers inside each one
    new_dictionary = {}
    for key, value in FLEET["environments"].items():
        total = 0
        for item in value:
            total = total + item["bytes_transferred"]
        new_dictionary[key] = total
    return new_dictionary

if __name__ == "__main__":
    for environment, total in bytes_per_environment().items():
        print(f"{environment}: {total:,} bytes")
