"""Check your subprocess and socket functions.

    python3 check_commands.py

Each check uses a port nobody else is on, so running this twice is safe.
"""

import socket
import subprocess
import sys
import time

import commands


def free_port():
    """Ask the OS for a port that is definitely unused right now."""
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def main() -> int:
    failures = 0
    core_started = True

    print("CORE - run_command()")
    result = commands.run_command([sys.executable, "--version"])
    if result is None:
        print("  SKIP  not started")
        core_started = False
    else:
        if getattr(result, "returncode", None) == 0:
            print("  PASS  ran python --version, returncode 0")
        else:
            print(f"  FAIL  returncode was {getattr(result, 'returncode', None)}")
            failures += 1
        text = (getattr(result, "stdout", "") or "") + (getattr(result, "stderr", "") or "")
        if isinstance(text, str) and "Python" in text:
            print("  PASS  captured the output as text")
        else:
            print(f"  FAIL  output was {text!r}")
            print("        Pass capture_output=True and text=True.")
            failures += 1

        try:
            commands.run_command(["definitely-not-a-real-program-xyz"])
        except FileNotFoundError as error:
            if "definitely-not-a-real-program-xyz" in str(error):
                print("  PASS  a missing program raises FileNotFoundError naming it")
            else:
                print(f"  FAIL  raised FileNotFoundError but did not name it: {error}")
                failures += 1
        except Exception as error:
            print(f"  FAIL  raised {type(error).__name__}, expected FileNotFoundError")
            failures += 1
        else:
            print("  FAIL  a missing program did not raise at all")
            failures += 1

    print("CORE - command_succeeded()")
    ok = commands.command_succeeded([sys.executable, "-c", "pass"])
    bad = commands.command_succeeded([sys.executable, "-c", "import sys; sys.exit(3)"])
    if ok is True and bad is False:
        print("  PASS  0 is success, 3 is failure")
    else:
        print(f"  FAIL  exit 0 gave {ok!r}, exit 3 gave {bad!r}")
        print("        Check result.returncode == 0. Do not parse the output.")
        failures += 1
        core_started = core_started and ok is not False

    print("EXTENSION - start, wait, check, stop")
    port = free_port()
    proc = commands.start_service(port=port)
    if proc is None:
        print("  SKIP  start_service not started")
    else:
        try:
            if commands.is_listening(port=port, timeout=0.3):
                print("  NOTE  the port answered immediately - unusual but fine")
            came_up = commands.wait_until_listening(port=port)
            if came_up:
                print("  PASS  waited for the service and it came up")
            else:
                print("  FAIL  wait_until_listening gave up before the service "
                      "started")
                print("        slow_service takes ~0.4s. Poll, do not check once.")
                failures += 1

            if commands.is_listening(port=port):
                print("  PASS  is_listening is True while it runs")
            else:
                print("  FAIL  is_listening is False while the service is running")
                failures += 1

            code = commands.stop_service(proc)
            if code is None:
                print("  FAIL  stop_service returned None")
                failures += 1
            else:
                print(f"  PASS  stopped it, return code {code}")

            if proc.poll() is None:
                print("  FAIL  the process is still running after stop_service")
                print("        Did you wait() after terminate()?")
                failures += 1

            time.sleep(0.2)
            if not commands.is_listening(port=port, timeout=0.3):
                print("  PASS  the port is free again")
            else:
                print("  FAIL  something is still listening on that port")
                failures += 1
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()

    print("STRETCH - check_detail()")
    detail = commands.check_detail("127.0.0.1", free_port())
    if not detail:
        print("  SKIP  not started - that is fine, core is the floor")
    else:
        if detail == "refused":
            print("  PASS  a closed port is 'refused'")
        else:
            print(f"  FAIL  a closed port gave {detail!r}, expected 'refused'")
            failures += 1
        bad_name = commands.check_detail("no-such-host.invalid", 80)
        if bad_name == "unresolvable":
            print("  PASS  a bad hostname is 'unresolvable'")
        else:
            print(f"  FAIL  a bad hostname gave {bad_name!r}, expected "
                  f"'unresolvable'")
            failures += 1

    print("STRETCH - can_ping()")
    try:
        pinged = commands.can_ping("127.0.0.1")
    except RuntimeError as error:
        print(f"  SKIP  {error}")
    except Exception as error:
        print(f"  FAIL  raised {type(error).__name__}: {error}")
        failures += 1
    else:
        if pinged is True:
            print("  PASS  localhost answers ping")
        elif pinged is False:
            print("  NOTE  localhost did not answer ping. If ICMP is blocked on "
                  "your network that is a real finding, not a bug in your code.")
        else:
            print(f"  FAIL  returned {pinged!r}, expected True or False")
            failures += 1

    print()
    if not core_started:
        print("Core tier not started yet. Fill in run_command() first.")
        return 1
    print(f"{failures} check(s) failed." if failures else "All attempted checks passed.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
