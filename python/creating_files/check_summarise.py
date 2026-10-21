"""Check your log summary.

    python3 check_summarise.py
"""

import sys
import tempfile
from pathlib import Path

import summarise

EXPECTED_LEVELS = {"INFO": 16, "WARN": 4, "ERROR": 3}
EXPECTED_HOSTS = ["api-01", "api-01-stg"]
EXPECTED_UNPARSEABLE = 2


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

    print("CORE - count_levels()")
    counts = summarise.count_levels()
    if counts == {"INFO": 0, "WARN": 0, "ERROR": 0}:
        print("  SKIP  not started")
        core_started = False
    else:
        failures += check("counts", counts, EXPECTED_LEVELS)
        if sum(counts.values()) == 25:
            print("        (that is all 25 lines - two of them are not "
                  "parseable, so the total should be 23)")

    print("EXTENSION - error_hosts()")
    hosts = summarise.error_hosts()
    if not hosts:
        print("  SKIP  not started")
    else:
        failures += check("hosts", sorted(hosts), EXPECTED_HOSTS)

    print("EXTENSION - write_summary()")
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "summary.txt"
        summarise.write_summary(out)
        if not out.exists():
            print("  SKIP  not started - nothing was written")
        else:
            text = out.read_text(encoding="utf-8")
            if not text.strip():
                print("  FAIL  the file was created but is empty")
                failures += 1
            elif all(str(v) in text for v in EXPECTED_LEVELS.values()):
                print("  PASS  summary written, contains all three counts")
            else:
                print(f"  FAIL  summary is missing some counts. Got:\n{text}")
                failures += 1

    print("STRETCH - unparseable_count()")
    bad = summarise.unparseable_count()
    if bad == 0:
        print("  SKIP  not started - that is fine, core is the floor")
    else:
        failures += check("unparseable", bad, EXPECTED_UNPARSEABLE)

    print()
    if not core_started:
        print("Core tier not started yet. Fill in count_levels() first.")
        return 1
    print(f"{failures} check(s) failed." if failures else "All attempted checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
