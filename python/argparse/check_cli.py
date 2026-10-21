"""Check your command-line tool.

    python3 check_cli.py
"""

import io
import json
import subprocess
import sys
from contextlib import redirect_stdout

import cli


def run(argv):
    """Run main() with these arguments, returning (exit_code, printed_text)."""
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            code = cli.main(argv)
    except SystemExit as error:
        code = error.code
    return code, buffer.getvalue()


def main() -> int:
    failures = 0

    print("CORE - the parser")
    parser = cli.build_parser()
    options = {action.dest for action in parser._actions}
    for name in ("config", "dry_run"):
        if name in options:
            print(f"  PASS  has --{name.replace('_', '-')}")
        else:
            print(f"  FAIL  no --{name.replace('_', '-')} argument")
            failures += 1

    if "config" not in options:
        print("\nCore tier not started yet. Add --config first.")
        return 1

    args = parser.parse_args([])
    if getattr(args, "config", None) == "deploy.yaml":
        print("  PASS  --config defaults to deploy.yaml")
    else:
        print(f"  FAIL  --config default was {getattr(args, 'config', None)!r}")
        failures += 1

    if getattr(args, "dry_run", None) is False:
        print("  PASS  --dry-run is False when absent")
    else:
        print(f"  FAIL  --dry-run was {getattr(args, 'dry_run', None)!r} when "
              f"absent; use action='store_true'")
        failures += 1

    print("CORE - exit codes")
    code, text = run([])
    if code == 0:
        print("  PASS  a valid config exits 0")
    else:
        print(f"  FAIL  a valid config exited {code}, expected 0")
        failures += 1
    if not text.strip():
        print("  FAIL  nothing was printed on a successful run")
        failures += 1

    code, text = run(["--config", "deploy_broken.yaml"])
    if code == 1:
        print("  PASS  an invalid config exits 1")
    else:
        print(f"  FAIL  an invalid config exited {code}, expected 1")
        failures += 1
    if "app_port" in text or "release_version" in text:
        print("  PASS  the problems are reported to the user")
    else:
        print("  FAIL  the output does not say what was wrong:")
        print(f"        {text.strip()[:120]}")
        failures += 1

    print("CORE - --dry-run")
    code, text = run(["--dry-run"])
    if code == 0 and text.strip():
        print("  PASS  --dry-run runs and says something")
    else:
        print(f"  FAIL  --dry-run exited {code} with output {text.strip()[:60]!r}")
        failures += 1

    print("EXTENSION - the shell gate")
    result = subprocess.run(
        [sys.executable, "-c",
         "import sys, cli; sys.exit(cli.main([]))"],
        capture_output=True, text=True, cwd=".",
    )
    if result.returncode == 0:
        print("  PASS  `python3 cli.py && echo OK` would fire")
    else:
        print(f"  FAIL  the process exited {result.returncode} on a valid config")
        failures += 1

    print("EXTENSION - --format json")
    if "format" not in options:
        print("  SKIP  no --format argument yet")
    else:
        code, text = run(["--format", "json"])
        try:
            json.loads(text)
        except json.JSONDecodeError:
            print("  FAIL  --format json did not produce valid JSON:")
            print(f"        {text.strip()[:120]}")
            failures += 1
        else:
            print("  PASS  --format json produces valid JSON")

    print("STRETCH - --verbose")
    if "verbose" in options:
        print("  PASS  has --verbose")
    else:
        print("  SKIP  no --verbose yet - that is fine, core is the floor")

    print()
    print(f"{failures} check(s) failed." if failures else "All attempted checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
