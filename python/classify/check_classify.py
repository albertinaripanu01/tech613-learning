"""Check your control flow answers.

    python3 check_classify.py
"""

import io
import sys
from contextlib import redirect_stdout

import classify

CLASSIFY_CASES = [
    (94, "CRITICAL"), (90, "CRITICAL"), (89, "WARNING"), (88, "WARNING"),
    (80, "WARNING"), (79, "OK"), (41, "OK"), (0, "OK"),
]
EXPECTED_COUNTS = {"CRITICAL": 1, "WARNING": 1, "OK": 5}
RETRY_CASES = [
    (([False, False, True], 5), (True, 3), "succeeds on the third attempt"),
    (([True], 5), (True, 1), "succeeds immediately"),
    (([False, False, False], 3), (False, 3), "never succeeds, budget 3"),
    (([False], 5), (False, 5), "fewer results than attempts allowed"),
    (([], 2), (False, 2), "no results at all"),
]


def main() -> int:
    failures = 0

    print("CORE - classify()")
    for value, expected in CLASSIFY_CASES:
        got = classify.classify(value)
        if got == expected:
            print(f"  PASS  {value}% -> {expected}")
        else:
            print(f"  FAIL  {value}% -> got {got!r}, expected {expected!r}")
            failures += 1

    print("CORE - print_report()")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        classify.print_report()
    lines = [line for line in buffer.getvalue().splitlines() if line.strip()]
    if len(lines) == len(classify.SERVERS):
        print(f"  PASS  printed {len(lines)} lines")
    else:
        print(f"  FAIL  printed {len(lines)} lines, expected {len(classify.SERVERS)}")
        failures += 1

    print("EXTENSION - count_states()")
    counts = classify.count_states()
    if counts == EXPECTED_COUNTS:
        print(f"  PASS  {counts}")
    elif sum(counts.values()) == len(classify.SERVERS):
        print(f"  FAIL  {counts}")
        print("        That is all 8 servers. Did you skip the one that is down?")
        failures += 1
    else:
        print(f"  FAIL  got {counts}, expected {EXPECTED_COUNTS}")
        failures += 1

    print("STRETCH - retry_until_healthy()")
    # Decide first whether it has been started at all, so a trainee who stopped
    # after core is not shown five alarming failures for work they did not do.
    started = any(
        tuple(classify.retry_until_healthy(*args)) != (False, 0)
        for args, _, _ in RETRY_CASES
    )
    if not started:
        print("  SKIP  not started - that is fine, core is the floor")
    else:
        for args, expected, label in RETRY_CASES:
            got = tuple(classify.retry_until_healthy(*args))
            if got == expected:
                print(f"  PASS  {label}")
            else:
                print(f"  FAIL  {label}: got {got!r}, expected {expected!r}")
                failures += 1

    print()
    print(f"{failures} check(s) failed." if failures > 0 else "All attempted checks passed.")
    return 1 if failures > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
