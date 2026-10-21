import logging
from pathlib import Path

# Choose the file where logs will be saved.
log_file = Path("deploy.log")

# A handler decides where log messages go.
# This handler displays INFO and more serious messages in the terminal.
console = logging.StreamHandler()
console.setLevel(logging.INFO)
print("------------------------")
# This handler writes DEBUG and more serious messages to deploy.log.
# By default, it appends messages, keeping logs from previous runs.
to_file = logging.FileHandler(log_file, encoding="utf-8")
to_file.setLevel(logging.DEBUG)

# Configure logging:
# - DEBUG allows all standard levels through to the handlers.
# - Each handler then applies its own level filter.
# - asctime: time of the message.
# - levelname: DEBUG, INFO, WARNING, ERROR or CRITICAL.
# - -8s: left-align the level in a field at least 8 characters wide.
# - name: logger name, which is "deploy" below.
# - message: the text you provide.
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s %(message)s",
    datefmt="%H:%M:%S",
    handlers=[console, to_file],
)

# Create a named logger for deployment messages.
log = logging.getLogger("deploy")

# These messages simulate a deployment; they do not deploy anything.

# DEBUG: diagnostic detail. Goes to the file only.
log.debug("Copying releases/v3 to app/current")

# INFO: normal progress. Goes to both the terminal and the file.
log.info("Config validated: deploying v3 to ~/app/current")
log.info("Backed up current release (v2)")
log.info("Stopped previous app (pid 41822)")

# Simulate five failed health checks.
limit = 5
status = 500

# range(1, limit + 1) gives 1, 2, 3, 4, 5.
for attempt in range(1, limit + 1):
    # WARNING: something went wrong, but the process continues.
    log.warning(
        f"Health check attempt {attempt}/{limit} failed: HTTP {status}"
    )

# ERROR: an operation failed.
log.error(f"Health check failed after {limit} attempts")

log.warning("Rolling back to v2...")
log.info("Rollback health check passed. Service restored on v2.")

# Demonstrate logging an exception with its traceback.
try:
    # This raises ValueError because the string is not a number.
    int("not-a-port")
except ValueError:
    # Logs an ERROR message plus the traceback showing where it failed.
    log.exception("Could not read the port from config")

# Demonstrate logging an error without its traceback.
try:
    int("not-a-port")
except ValueError as error:
    # "error" holds the exception, so we can include its description.
    log.error(f"Could not read the port: {error}")

# Ensure any buffered log text is written before reading the file.
to_file.flush()

# Read and display the saved logs, including DEBUG messages.
print("--- what landed in the file ---")
print(log_file.read_text(encoding="utf-8"), end="")
print("--- end of file ---")

# Flush and close the logging handlers.
logging.shutdown()