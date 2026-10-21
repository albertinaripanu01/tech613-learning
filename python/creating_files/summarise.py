"""Lab - summarise a log file.

app.log is in this folder. It is 25 lines of a realistic morning: startups,
health checks, a slow query, two upstream timeouts, a rejected deploy, a disk
warning and a shutdown.

Two of those lines cannot be parsed. That is deliberate.

Run  python3 check_summarise.py  to test.
"""
from collections import Counter
from pathlib import Path

LOG = Path(__file__).parent / "app.log"
LEVELS = ("INFO", "WARN", "ERROR")


def count_levels():
    """CORE - count how many lines are at each level.

    A parseable line looks like this, with uneven spacing:

        2026-09-14 06:00:11,204 INFO  [web-01] 10.24.9.40 GET /health 200 4ms
        ^ date     ^ time      ^ level ^ host

    Use .split() rather than counting characters - the spacing is not
    consistent and that is on purpose.

    Skip any line whose third field is not one of LEVELS.

    Returns:
        dict with a key per level, e.g. {"INFO": 0, "WARN": 0, "ERROR": 0}
    """

    # TODO: open the log with a context manager and an explicit encoding,
    # loop over its lines, and count.
    counts={"INFO": 0, "WARN": 0, "ERROR": 0}
    with open("app.log", encoding="utf-8") as file:
        for line in file:
            if "ERROR" in line:
                counts["ERROR"] += 1
            if "INFO" in line:
                counts["INFO"] += 1
            if "WARN" in line:
                counts["WARN"] += 1
    return counts


def error_hosts():
    """EXTENSION - return the hostnames that produced an ERROR.

    The host field looks like [api-01]. Strip the square brackets.

    Returns:
        a sorted list of unique hostnames
    """
    hosts=[]
    with open("app.log", encoding="utf-8") as file:
        for line in file:
            if "ERROR" in line:
                hostname = line.split("[", 1)[1].split("]", 1)[0]
                if hostname not in hosts:
                    hosts.append(hostname)
    # TODO
    return sorted(hosts)


def write_summary(path):
    """EXTENSION - write the summary to a file instead of printing it.

    Write to the path given. Suggested shape, but yours may differ:

        INFO 16
        WARN 4
        ERROR 3
        errors from: api-01, api-01-stg

    Remember that file.write does not add a newline for you, and that "w"
    truncates the file before writing.

    Args:
        path: a pathlib.Path to write to
    """
    counted = count_levels()
    hosts=error_hosts()
    with open("report.txt", "w", encoding="utf-8") as file:
        for item,key in counted.items():
            file.write(f"{item} {key}\n")
        for item in hosts:
            file.write(f"{item}\n")
    print(Path("report.txt").read_text(encoding="utf-8"))
    # TODO
    pass


def unparseable_count():
    """STRETCH - count the lines this script could not parse.

    A script that crashes on line 12 of a log file is worse than no script.
    Count them, do not crash on them.

    Returns:
        int
    """
    counted=0
    with open("app.log", encoding="utf-8") as file:
        for line in file:
            if not any(level in line for level in LEVELS):
                counted=counted+1
    return counted


if __name__ == "__main__":
    print(count_levels())
    print(error_hosts())
    print(f"{unparseable_count()} unparseable lines")
