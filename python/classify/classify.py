"""Lab - classify servers, count states, and retry.

Run  python3 check_classify.py  to test.
"""
from logging import critical
from operator import truediv

SERVERS = [
    {"hostname": "web-01", "status": "healthy", "disk_percent_used": 41},
    {"hostname": "web-02", "status": "healthy", "disk_percent_used": 38},
    {"hostname": "api-01", "status": "degraded", "disk_percent_used": 88},
    {"hostname": "api-02", "status": "healthy", "disk_percent_used": 52},
    {"hostname": "db-01", "status": "healthy", "disk_percent_used": 73},
    {"hostname": "web-01-stg", "status": "healthy", "disk_percent_used": 19},
    {"hostname": "api-01-stg", "status": "down", "disk_percent_used": 22},
    {"hostname": "build-01", "status": "healthy", "disk_percent_used": 94},
]

CRITICAL_AT = 90
WARNING_AT = 80


def classify(disk_percent_used):
    """CORE - return "CRITICAL", "WARNING" or "OK" for a disk percentage.

    At or above CRITICAL_AT  -> "CRITICAL"
    At or above WARNING_AT   -> "WARNING"
    Otherwise                -> "OK"

    Watch the order of your branches.

    Returns:
        str
    """
    # TODO: write the if/elif/else chain
    if disk_percent_used >= CRITICAL_AT:
        return "CRITICAL"
    elif disk_percent_used >= WARNING_AT:
        return "WARNING"
    else:
        return "OK"


def print_report():
    """CORE - print one line per server: hostname and its classification.

        web-01 OK
    """
    # TODO: loop over SERVERS and print each hostname and its classification
    for item in SERVERS:
        print(f'{item["hostname"]} {classify(item["disk_percent_used"])}')


def count_states():
    """EXTENSION - count servers in each state, skipping any that are down.

    Use `continue` to skip a server whose status is "down" - a machine that is
    not running has no meaningful disk reading.

    Returns:
        dict, e.g. {"CRITICAL": 0, "WARNING": 0, "OK": 0}
    """
    counts = {"CRITICAL": 0, "WARNING": 0, "OK": 0}
    for item in SERVERS:
        if  item["status"]=="down":
            continue
        classification = classify(item["disk_percent_used"])
        counts[classification] += 1

    # TODO: loop, skip the down servers, and count the rest
    return counts


def retry_until_healthy(results, max_attempts):
    """STRETCH - the retry loop from the lesson, and stage 5 of Friday's project.

    `results` stands in for repeated calls to a real health check. Each item is
    True (healthy) or False (not yet).

    Try up to max_attempts times. Stop as soon as one succeeds.

    Returns:
        tuple of (healthy, attempts_used)
        e.g. (True, 3) if the third attempt succeeded
             (False, 5) if five attempts were allowed and none succeeded

    Note: you may be given fewer results than max_attempts. Treat a missing
    result as a failure rather than crashing.
    """
    attempts = 1
    while attempts<=max_attempts:
        if attempts <= len(results) and results[attempts-1]==True:
            return (True, attempts)
        attempts=attempts+1

    # TODO: write the while loop
    return (False, max_attempts)


if __name__ == "__main__":
    print_report()
    print()
    print(count_states())
    print(retry_until_healthy([False, False, True], 5))
