"""Lab - convert a deployment script from print to logging.

This simulates the deployment you will write for real on Friday. Nothing here
touches the filesystem or the network; the point is the logging, not the deploy.

Every print below is in the wrong place. Replace each with a log call at the
right level, and configure a logger at the top.

Run  python3 check_logging.py  to test.
"""
import logging
import sys
import time
from pathlib import Path

HERE = Path(__file__).parent
LOG_FILE = HERE / "deploy.log"
verbose = "--verbose" in sys.argv
console = logging.StreamHandler()
console.setLevel(logging.DEBUG if verbose else logging.INFO)
to_file = logging.FileHandler(LOG_FILE, encoding="utf-8")
to_file.setLevel(logging.DEBUG)
# TODO (CORE): configure logging here.
#   - a format with a timestamp, the level, and the message
#   - a module-level logger:  log = logging.getLogger("deploy")
logging.basicConfig(
level=logging.DEBUG,
format="%(asctime)s %(levelname)-8s %(name)s %(message)s",
datefmt="%H:%M:%S",
handlers=[console, to_file],)

# TODO (EXTENSION): console at INFO, LOG_FILE at DEBUG, both at once.
#
# TODO (STRETCH): make `verbose` switch the console handler to DEBUG.


def deploy(version="v3", verbose=False, fail_health_check=True):
    """Simulate a deployment. Returns an exit code.

    Levels to use, in order of appearance:

        starting                      INFO
        reading the config            DEBUG
        config validated              INFO
        backed up the release         INFO
        stopped the old process       INFO
        copying files                 DEBUG
        started the new process       INFO
        each failed health check      WARNING
        health check finally failed   ERROR
        rolling back                  WARNING
        rollback health check passed  INFO
        rollback health check failed  CRITICAL
    """
    print(f"deploy.py starting, pid {12345}")
    print("Reading config from deploy.yaml")
    print(f"Config validated: deploying {version}")
    print("Backed up current release (v2)")
    print("Stopped previous app (pid 41822)")
    print(f"Copying releases/{version} to app/current")
    print("Started new app (pid 41903)")

    healthy = not fail_health_check
    for attempt in range(1, 6):
        if healthy:
            print(f"Health check attempt {attempt}/5 passed")
            break
        print(f"Health check attempt {attempt}/5 failed: HTTP 500")
    else:
        print("Health check failed after 5 attempts, last status HTTP 500")
        print("Rolling back to v2")
        print("Stopped failed app (pid 41903)")
        print("Started app from backup (pid 41940)")
        print("Rollback health check passed. Service restored on v2.")
        return 2

    print(f"Deployment of {version} complete")
    return 0


def parse_port(raw):
    """STRETCH - used by the exception-logging part of the lab.

    Wrap the int() in try/except and use log.exception so the traceback lands
    in the file. Return None when it cannot be parsed.
    """
    return int(raw)


if __name__ == "__main__":
    sys.exit(deploy())
