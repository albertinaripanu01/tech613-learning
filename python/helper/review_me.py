"""Four functions, as an AI assistant produced them.

They were generated from reasonable prompts. They all run. They all look
plausible. Reviewing code like this is a real part of a junior engineer's job,
and it starts here.

FOR EACH FUNCTION:
  1. Write a comment saying what you think it does.
  2. Predict what the demo at the bottom will print.
  3. Run the file and compare.

Do not fix anything yet. Find the problems first.

Nobody is telling you how many there are.

    python3 review_me.py
"""


# --------------------------------------------------------------------------
# 1. Prompt: "write a function that returns the port for a server dict"
# --------------------------------------------------------------------------
def get_port(server):
    if "port" in server:
        return server["port"]
    return None


# --------------------------------------------------------------------------
# 2. Prompt: "write a function that collects the names of failing hosts"
# --------------------------------------------------------------------------
def collect_failures(hostname, failures=[]):
    failures.append(hostname)
    return failures


# --------------------------------------------------------------------------
# 3. Prompt: "write a function that says whether a disk is critically full"
# --------------------------------------------------------------------------
def is_critical(disk_used, threshold=90):
    if disk_used > threshold:
        return True
    else:
        return False


# --------------------------------------------------------------------------
# 4. Prompt: "write a function that turns a config value into a port number"
# --------------------------------------------------------------------------
def parse_port(raw_value):
    try:
        return int(raw_value)
    except Exception:
        pass


if __name__ == "__main__":
    print("1.", get_port({"hostname": "web-01", "port": 8801}))
    print("1.", get_port({"hostname": "web-01"}))

    print("2.", collect_failures("api-01"))
    print("2.", collect_failures("db-01"))

    print("3.", is_critical(94))
    print("3.", is_critical(90))

    print("4.", parse_port("8801"))
    print("4.", parse_port("not-a-port"))
