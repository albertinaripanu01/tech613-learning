"""Lab - write four functions from their docstrings.

This is the shape of Friday's starter repository: a docstring says what the
function must do, and a TODO marks where the work goes. Your teammates will be
working against the contract in the docstring, not against your code.

Run  python3 check_helpers.py  to test.
"""


def is_healthy(status_code):
    """CORE - return True if a status code counts as healthy.

    Healthy means 200 or 204. Anything else is not healthy.

    Args:
        status_code: an HTTP status code, as an int

    Returns:
        bool
    """
    # TODO
    if status_code == 200 or status_code == 204:
        return True
    return False


def classify_disk(disk_used, critical_at=90, warning_at=80):
    """CORE - return "CRITICAL", "WARNING" or "OK" for a disk percentage.

    At or above critical_at -> "CRITICAL"
    At or above warning_at  -> "WARNING"
    Otherwise               -> "OK"

    Note "at or above", not "above". The review activity had a function that got
    this wrong.

    Args:
        disk_used: percentage of disk used, as a number
        critical_at: threshold for CRITICAL
        warning_at: threshold for WARNING

    Returns:
        str
    """
    # TODO
    if disk_used < warning_at:
        return "OK"
    elif disk_used>= warning_at and disk_used < critical_at:
        return "WARNING"
    elif disk_used>= critical_at:
        return "CRITICAL"


def format_log_line(level, hostname, message):
    """CORE - return a log line as a string. Do not print it.

    Format, with single spaces:

        INFO web-01 health check passed

    The level is upper case. Returning rather than printing is what lets this
    be tested, which you will do tomorrow.

    Args:
        level: "info", "warn" or "error", in any case
        hostname: the host the message is about
        message: what happened

    Returns:
        str
    """
    # TODO
    return f"{level.upper()} {hostname} {message}"


def summarise_inventory(servers, counts={}):
    """EXTENSION - count how many servers are in each disk state.

    Returns a dict with all three keys always present, even when a count is
    zero:

        {"CRITICAL": <int>, "WARNING": <int>, "OK": <int>}

    Use classify_disk. Skip any server whose status is "down".

    THIS FUNCTION HAS A BUG IN ITS SIGNATURE. It is the same bug you met in the
    review activity. Find it and fix it before you write the body - if you do
    not, your second call will return the wrong answer and the checker will tell
    you so without telling you why.

    Args:
        servers: a list of server dicts
        counts: (see above)

    Returns:
        dict
    """
    # TODO
    return counts


# STRETCH
#
# Add type hints to all four functions. A hint looks like this:
#
#     def is_healthy(status_code: int) -> bool:
#
# Then answer this, in a comment at the bottom of this file:
#
#   Python does not check type hints at runtime. Calling is_healthy("200") with
#   a string still runs. So what are they for, and what would actually catch
#   that mistake?
#
# Bring your answer to tomorrow's consolidation session.

if __name__ == "__main__":
    print(is_healthy(200))
    print(classify_disk(94))
    print(format_log_line("info", "web-01", "health check passed"))
