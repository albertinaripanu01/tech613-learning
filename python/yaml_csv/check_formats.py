"""Check your three-format loader.

    python3 check_formats.py
"""

import csv
import sys
import tempfile
from pathlib import Path

import formats

EXPECTED_SERVERS = 8
EXPECTED_SUMMARY = [
    {"environment": "production", "servers": 5, "bytes": 47516028},
    {"environment": "staging", "servers": 2, "bytes": 402117},
    {"environment": "tooling", "servers": 1, "bytes": 630885},
]


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

    print("CORE - the three loaders")
    loaders = {
        "load_json": formats.load_json,
        "load_yaml": formats.load_yaml,
        "load_csv": formats.load_csv,
    }
    loaded = {}
    for name, fn in loaders.items():
        rows = fn()
        loaded[name] = rows
        if not rows:
            print(f"  SKIP  {name} not started")
            core_started = False
        else:
            failures += check(f"{name} returns {EXPECTED_SERVERS} servers",
                              len(rows), EXPECTED_SERVERS)

    if all(loaded.values()):
        csv_rows = loaded["load_csv"]
        first = csv_rows[0]
        if isinstance(first.get("port"), int):
            print("  PASS  load_csv converted the numeric fields")
        else:
            print(f"  FAIL  load_csv left port as {first.get('port')!r} "
                  f"({type(first.get('port')).__name__})")
            print("        CSV has no types. Convert the NUMERIC_FIELDS to int.")
            failures += 1

    print("CORE - all_three_match()")
    if not any(loaded.values()):
        print("  SKIP  not started")
    else:
        result = formats.all_three_match()
        if result is True:
            print("  PASS  all three formats hold identical data")
        else:
            print(f"  FAIL  all_three_match() returned {result!r}")
            print("        If this is False, compare one record from each and "
                  "look at the types.")
            failures += 1

    print("EXTENSION - summarise_by_environment()")
    summary = formats.summarise_by_environment()
    if not summary:
        print("  SKIP  not started")
    else:
        failures += check("summary", summary, EXPECTED_SUMMARY)

    print("EXTENSION - write_summary_csv()")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "summary.csv"
        formats.write_summary_csv(out)
        if not out.exists():
            print("  SKIP  not started")
        else:
            with open(out, newline="", encoding="utf-8") as file:
                rows = list(csv.DictReader(file))
            if len(rows) == 3:
                print("  PASS  wrote 3 rows with a header")
            else:
                print(f"  FAIL  read back {len(rows)} row(s), expected 3")
                print("        Did you call writeheader()?")
                failures += 1

    print()
    if not core_started:
        print("Core tier not started yet.")
        return 1
    print(f"{failures} check(s) failed." if failures else "All attempted checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
