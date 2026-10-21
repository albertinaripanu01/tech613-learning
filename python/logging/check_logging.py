"""Check your logging conversion.

    python3 check_logging.py

This inspects the log records your script emits, rather than its printed output.
If you are still using print, nothing is recorded and the first check tells you.
"""

import io
import logging
import sys
from contextlib import redirect_stdout

import deploy_log


class Capture(logging.Handler):
    """Collect every record emitted anywhere, at any level."""

    def __init__(self):
        super().__init__(level=logging.DEBUG)
        self.records = []

    def emit(self, record):
        self.records.append(record)


def run_capturing(**kwargs):
    """Run deploy() and return (log records, printed text)."""
    capture = Capture()
    root = logging.getLogger()
    previous_level = root.level
    root.addHandler(capture)
    root.setLevel(logging.DEBUG)
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            deploy_log.deploy(**kwargs)
    finally:
        root.removeHandler(capture)
        root.setLevel(previous_level)
    return capture.records, buffer.getvalue()


def levels_used(records):
    return {record.levelname for record in records}


def main() -> int:
    failures = 0

    print("CORE - deploy() logs instead of printing")
    records, printed = run_capturing()
    if not records:
        print("  FAIL  no log records were emitted at all")
        print("        Still using print? Replace them with log.info and friends.")
        return 1
    print(f"  PASS  emitted {len(records)} log records")

    leftover = [line for line in printed.splitlines() if line.strip()]
    if leftover:
        print(f"  FAIL  {len(leftover)} line(s) still printed rather than logged:")
        for line in leftover[:3]:
            print(f"          {line}")
        failures += 1
    else:
        print("  PASS  nothing is printed any more")

    print("CORE - the right levels are used")
    used = levels_used(records)
    for level in ("INFO", "WARNING", "ERROR"):
        if level in used:
            print(f"  PASS  uses {level}")
        else:
            print(f"  FAIL  never uses {level}")
            failures += 1

    if "DEBUG" in used:
        print("  PASS  uses DEBUG for the detail lines")
    else:
        print("  FAIL  never uses DEBUG")
        print("        'Reading config' and 'Copying releases' are DEBUG.")
        failures += 1

    print("CORE - levels are on the right messages")
    by_level = {}
    for record in records:
        by_level.setdefault(record.levelname, []).append(record.getMessage().lower())

    warnings = " ".join(by_level.get("WARNING", []))
    if "attempt" in warnings:
        print("  PASS  a failed health check attempt is a WARNING")
    else:
        print("  FAIL  the failed attempts should be WARNING, not INFO or ERROR")
        print("        They are wrong but handled - the retry loop carries on.")
        failures += 1

    errors = " ".join(by_level.get("ERROR", []))
    if "after 5 attempts" in errors or "failed after" in errors:
        print("  PASS  giving up after 5 attempts is an ERROR")
    else:
        print("  FAIL  'failed after 5 attempts' should be ERROR")
        failures += 1

    print("CORE - a successful deployment logs no errors")
    ok_records, _ = run_capturing(fail_health_check=False)
    bad = [r for r in ok_records if r.levelno >= logging.ERROR]
    if not bad:
        print("  PASS  a clean run produces nothing at ERROR or above")
    else:
        print(f"  FAIL  a clean run logged {len(bad)} record(s) at ERROR or above:")
        for r in bad[:3]:
            print(f"          {r.levelname} {r.getMessage()}")
        failures += 1

    print("EXTENSION - a log file is written")
    log_file = deploy_log.LOG_FILE
    if log_file.exists() and log_file.stat().st_size > 0:
        text = log_file.read_text(encoding="utf-8")
        print(f"  PASS  {log_file.name} exists with {len(text.splitlines())} lines")
        if "DEBUG" in text:
            print("  PASS  the file has DEBUG lines in it")
        else:
            print("  FAIL  the file has no DEBUG lines")
            print("        Logger at DEBUG, console handler at INFO, file at DEBUG.")
            failures += 1
    else:
        print("  SKIP  no deploy.log yet - that is the extension tier")

    print()
    print(f"{failures} check(s) failed." if failures else "All attempted checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
