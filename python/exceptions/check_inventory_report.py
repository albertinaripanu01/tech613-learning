"""Check your JSON inventory report.

    python3 check_inventory_report.py
"""

import json
import sys
import tempfile
from pathlib import Path

import inventory_report as report

HERE = Path(__file__).parent
GOOD_SUMMARY = {"total": 8, "production": 5, "bytes": 48549030}
SAFE_SUMMARY = {"total": 5, "production": 3, "bytes": 31284435}
SKIPPED_HOSTS = ["api-01", "api-01-stg", "db-01"]
EMPTY = {"total": 0, "production": 0, "bytes": 0}


def check(label, got, want):
    if got == want:
        print(f"  PASS  {label}")
        return 0
    print(f"  FAIL  {label}")
    print(f"        got      {got!r}")
    print(f"        expected {want!r}")
    return 1


def main() -> int:
    failures = 0
    core_started = True

    print("CORE - load_inventory()")
    data = report.load_inventory(report.GOOD)
    if not data:
        print("  SKIP  not started")
        core_started = False
    else:
        failures += check("site key", data.get("site"), "eu-west")
        failures += check("server count", len(data.get("servers", [])), 8)

    print("CORE - summarise()")
    summary = report.summarise(report.GOOD)
    if summary == EMPTY:
        print("  SKIP  not started")
        core_started = False
    else:
        failures += check("summary of the good file", summary, GOOD_SUMMARY)

    print("EXTENSION - summarise_safely()")
    safe, skipped = report.summarise_safely(report.BROKEN)
    if safe == EMPTY and not skipped:
        print("  SKIP  not started")
    else:
        failures += check("summary of the broken file", safe, SAFE_SUMMARY)
        got_hosts = sorted(h for h, _ in skipped)
        failures += check("skipped hostnames", got_hosts, SKIPPED_HOSTS)
        if skipped and all(r for _, r in skipped):
            print("  PASS  every skipped record has a reason")
        else:
            print("  FAIL  some skipped records have no reason given")
            print("        A log that says what was skipped but not why is not "
                  "much use at 3am.")
            failures += 1

    print("STRETCH - write_report()")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "report.json"
        report.write_report(out, safe, skipped)
        if not out.exists():
            print("  SKIP  not started - that is fine, core is the floor")
        else:
            try:
                loaded = json.loads(out.read_text(encoding="utf-8"))
            except json.JSONDecodeError as error:
                print(f"  FAIL  the report you wrote is not valid JSON: {error}")
                failures += 1
            else:
                print("  PASS  report round-trips as valid JSON")
                if any("generated" in k or "timestamp" in k for k in loaded):
                    print("  PASS  report has a timestamp")
                else:
                    print("  FAIL  report has no timestamp field")
                    failures += 1

    print()
    if not core_started:
        print("Core tier not started yet.")
        return 1
    print(f"{failures} check(s) failed." if failures else "All attempted checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
