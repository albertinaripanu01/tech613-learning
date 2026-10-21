"""Lab - run commands, start and stop a service, and check whether it is up.

The extension tier is stages 3, 4 and 5 of Friday's deployment automator.

Run  python3 check_commands.py  to test.
"""

import platform
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
SERVICE = HERE / "slow_service.py"


def run_command(command, timeout=10):
    """CORE - run a command and return the completed process.

    `command` is a LIST, never a string, and never shell=True.

    Capture stdout and stderr as text. Pass the timeout through.

    If the program is not installed, raise FileNotFoundError with a message
    naming it - use shutil.which to check first, so the caller gets something
    readable rather than a bare OSError.

    Args:
        command: list of strings, e.g. [sys.executable, "--version"]
        timeout: seconds before giving up

    Returns:
        subprocess.CompletedProcess
    """
    # TODO
    return None


def command_succeeded(command, timeout=10):
    """CORE - True if the command exited 0.

    Zero means success. Anything else means failure. Do not parse the output.

    Returns:
        bool
    """
    # TODO
    return False


def start_service(port=8801):
    """EXTENSION - start slow_service.py in the background and return the Popen.

    Use Popen, not run - run would wait forever, because the service never
    finishes.

    Returns:
        subprocess.Popen
    """
    # TODO
    return None


def is_listening(host="127.0.0.1", port=8801, timeout=2.0):
    """EXTENSION - True if something accepts a TCP connection on host:port.

    Returns:
        bool
    """
    # TODO
    return False


def wait_until_listening(host="127.0.0.1", port=8801, attempts=10, delay=0.2):
    """EXTENSION - poll until the port answers, or give up.

    The service takes a moment to start. Checking once immediately after
    starting it will usually fail, which is why this exists.

    This is the same shape as Friday's health-check retry loop, and the same
    shape as a Kubernetes readiness probe in Week 8.

    Returns:
        True if it came up within the budget, False if it never did
    """
    # TODO
    return False


def stop_service(proc, timeout=5):
    """EXTENSION - stop a process started by start_service.

    Ask politely first, wait for it, and only force it if it will not go.
    Always wait after terminating - otherwise you carry on while the port is
    still held, and the replacement cannot bind to it.

    Returns:
        the process's return code
    """
    # TODO
    return None


def check_detail(host, port, timeout=2.0):
    """STRETCH - say WHY a connection failed, not just that it did.

    Returns one of:
        "up"
        "refused"        nothing listening on that port
        "timed out"      dropped, probably a firewall
        "unresolvable"   DNS could not find that name
        "error: ..."     anything else, with the message

    Down is not one thing, and telling them apart is most of the value of a
    health check.

    Returns:
        str
    """
    # TODO
    return ""


def can_ping(host, timeout=5):
    """STRETCH - True if the host answers a single ICMP echo request.

    The count flag differs by platform: -n on Windows, -c everywhere else.
    Use platform.system() to choose.

    Check the RETURN CODE, never the output - ping's text changes with the
    machine's language settings.

    Raise RuntimeError if ping is not installed.

    Returns:
        bool
    """
    # TODO
    return False


if __name__ == "__main__":
    print("python version:", run_command([sys.executable, "--version"]))

    proc = start_service()
    if proc is not None:
        print("came up:", wait_until_listening())
        print("stopped:", stop_service(proc))
