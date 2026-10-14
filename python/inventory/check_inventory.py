"""Check your inventory answers.

    python3 check_inventory.py

It tests the values your functions return, not how you wrote them. The stretch
part is skipped if you have not started it.
"""

import io
import sys
from contextlib import redirect_stdout

import inventory

EXPECTED_PRODUCTION = 5
EXPECTED_TOTAL = 48549030
EXPECTED_BUSIEST = "api-01"
EXPECTED_PER_ENV = {"production": 47516028, "staging": 402117, "tooling": 630885}


def report(label, got, want):
    if got == want:
        print(f"  PASS  {label}")
        return 0
    print(f"  FAIL  {label}: got {got!r}, expected {want!r}")
    return 1


def main() -> int:
    failures = 0

    print("CORE")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        inventory.list_servers(inventory.SERVERS)
    lines = [line for line in buffer.getvalue().splitlines() if line.strip()]
    if len(lines) == len(inventory.SERVERS):
        print(f"  PASS  list_servers printed {len(lines)} lines")
    else:
        print(f"  FAIL  list_servers printed {len(lines)} lines, "
              f"expected {len(inventory.SERVERS)}")
        failures += 1
    failures += report("count_production", inventory.count_production(inventory.SERVERS),
                       EXPECTED_PRODUCTION)

    print("EXTENSION")
    failures += report("total_bytes", inventory.total_bytes(inventory.SERVERS), EXPECTED_TOTAL)
    failures += report("busiest_host", inventory.busiest_host(inventory.SERVERS), EXPECTED_BUSIEST)

    print("STRETCH")
    try:
        import inventory_nested
    except ImportError:
        print("  SKIP  inventory_nested.py not found")
        return 1 if failures else 0

    result = inventory_nested.bytes_per_environment()
    if not result:
        print("  SKIP  bytes_per_environment not written yet")
    else:
        failures += report("bytes_per_environment", result, EXPECTED_PER_ENV)

    print()
    if failures:
        print(f"{failures} check(s) failed.")
    else:
        print("All attempted checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
