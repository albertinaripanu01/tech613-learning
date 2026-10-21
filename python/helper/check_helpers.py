"""Check your helpers.

    python3 check_helpers.py
"""

import sys

import helpers

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
EXPECTED_SUMMARY = {"CRITICAL": 1, "WARNING": 1, "OK": 5}


def check(label, got, want):
    if got == want:
        print(f"  PASS  {label}")
        return 0
    print(f"  FAIL  {label}: got {got!r}, expected {want!r}")
    return 1


def main() -> int:
    failures = 0

    print("CORE - is_healthy()")
    for code, want in [(200, True), (204, True), (500, False), (404, False),
                       (301, False)]:
        failures += check(f"is_healthy({code})", helpers.is_healthy(code), want)

    print("CORE - classify_disk()")
    for used, want in [(94, "CRITICAL"), (90, "CRITICAL"), (89, "WARNING"),
                       (80, "WARNING"), (79, "OK"), (0, "OK")]:
        failures += check(f"classify_disk({used})",
                          helpers.classify_disk(used), want)

    print("CORE - format_log_line()")
    failures += check(
        "format_log_line",
        helpers.format_log_line("info", "web-01", "health check passed"),
        "INFO web-01 health check passed",
    )
    failures += check(
        "format_log_line uppercases the level",
        helpers.format_log_line("ERROR", "api-01", "timed out"),
        "ERROR api-01 timed out",
    )

    print("EXTENSION - summarise_inventory()")
    # dict(...) takes a copy. Without it, a function still carrying the mutable
    # default returns the SAME object twice, and the two results compare equal
    # no matter what happened in between.
    first = dict(helpers.summarise_inventory(SERVERS))
    if first == {"CRITICAL": 0, "WARNING": 0, "OK": 0} or not first:
        print("  SKIP  not started - that is fine, core is the floor")
    else:
        failures += check("first call", first, EXPECTED_SUMMARY)
        # Call it a second time. If the mutable default is still there, the
        # counts carry over and every number doubles.
        second = dict(helpers.summarise_inventory(SERVERS))
        if second == EXPECTED_SUMMARY:
            print("  PASS  called twice, still correct")
        else:
            print(f"  FAIL  called twice: got {second!r}, "
                  f"expected {EXPECTED_SUMMARY!r}")
            print("        The counts carried over from the first call.")
            print("        Read the warning in the docstring again.")
            failures += 1

    print()
    print(f"{failures} check(s) failed." if failures else "All attempted checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
