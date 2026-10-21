# subprocess runs other programs. socket makes network connections.
# sys gives access to information about the running Python interpreter.
# These modules are built into Python; no installation is needed.

import os
import socket
import subprocess
import sys


def process_examples():
    # 1. Run a program and collect its output.
    # sys.executable is the path to the Python interpreter running this file.
    # A list keeps the program and its arguments separate.
    result = subprocess.run(
        [sys.executable, "--version"],
        capture_output=True,
        text=True,
    )

    # capture_output=True collects stdout and stderr instead of displaying them.
    # text=True gives us strings instead of bytes.
    # returncode is the exit status: 0 normally means success.
    print(result.returncode)
    # stdout is normal output. strip removes surrounding whitespace/newlines.
    print(result.stdout.strip())

    # 2. Run a command through a shell.
    # shell=True lets the shell interpret a command string, including special
    # characters such as pipes and semicolons (depending on the shell).
    # The classroom example uses Unix commands: ls -l /tmp.
    # Windows uses dir with cmd.exe instead.
    if os.name == "nt":
        result = subprocess.run(
            "dir", shell=True, capture_output=True, text=True
        )
    else:
        result = subprocess.run(
            "ls -l /tmp", shell=True, capture_output=True, text=True
        )
    print(result.stdout.strip() or result.stderr.strip())
    # On macOS, /tmp may be a symbolic link to private/tmp.
    # A symbolic link is a path that points to another location.

    # 3. Understand why inserting input into a shell command is dangerous.
    hostname = "web-01; rm -rf /tmp/something-important"
    command = f"ping {hostname}"
    print(f"the shell would run: {command}")
    # This string is ONLY printed, never executed.
    # In a Unix shell, ; separates commands. The injected second command would
    # try to delete a directory tree. This is called shell injection.

    # 4. Keep the input as one argument instead.
    command = ["ping", hostname]
    print(f"{len(command)} arguments:")
    for part in command:
        # !r shows the string representation, including quotes.
        print(f"  {part!r}")

    # shell=False is the default when running this list.
    # The entire hostname string becomes one argument; the semicolon does not
    # start another shell command. ping will normally reject this hostname.
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=3
        )
        print(result.returncode)
        # stderr is error output. 'or' selects it if stdout is empty.
        print(result.stdout.strip() or result.stderr.strip())
    except FileNotFoundError:
        print("The ping program could not be found.")
    except subprocess.TimeoutExpired:
        print("Ping did not finish within 3 seconds.")

    # 5. Check the return code yourself.
    # -c tells Python to execute the code supplied in the following argument.
    # sys.exit(3) deliberately ends that child process with exit code 3.
    result = subprocess.run(
        [sys.executable, "-c", "import sys; sys.exit(3)"],
        capture_output=True,
        text=True,
    )
    print(f"returncode: {result.returncode}")
    if result.returncode != 0:
        print("that command failed")

    # 6. Ask Python to raise an exception for a nonzero exit code.
    # Without check=True, a nonzero exit code alone does not raise this error.
    try:
        subprocess.run(
            [sys.executable, "-c", "import sys; sys.exit(1)"],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as error:
        print(f"raised: return code {error.returncode}")

    # 7. Stop waiting when a command takes too long.
    # The child tries to sleep for 10 seconds, but timeout=1 limits the wait.
    # subprocess.run kills and waits for the child before raising this error.
    try:
        subprocess.run(
            [sys.executable, "-c", "import time; time.sleep(10)"],
            timeout=1,
        )
    except subprocess.TimeoutExpired:
        print("gave up after 1 second")


def is_listening(host, port, timeout=2.0):
    """Return True if a TCP connection to host:port succeeds."""
    # host identifies the machine. port identifies a service on that machine.
    # timeout is the connection timeout in seconds.
    try:
        with socket.create_connection((host, port), timeout=timeout):
            # The with block closes the connection automatically.
            return True
    except OSError:
        # Network errors such as refused connections and name lookup failures
        # inherit from OSError, so this catches them together.
        return False


def check(host, port, timeout=2.0):
    """Describe whether a TCP connection succeeds or why it fails."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "up"
    # Specific exceptions must come before OSError, their general parent.
    except socket.timeout:
        return "timed out"
    except socket.gaierror:
        # Name resolution translates a hostname into an IP address.
        return "cannot resolve that name"
    except ConnectionRefusedError:
        return "refused - nothing listening"
    except OSError as error:
        return f"failed: {error}"
    # A successful TCP connection shows that something accepted it.
    # It does not prove that the application itself is healthy.


if __name__ == "__main__":
    # This block runs when you execute the file, but not when you import it.
    process_examples()

    # 127.0.0.1 means this computer. Port 9 may have no service listening.
    # Results depend on your machine and network.
    print(is_listening("127.0.0.1", 9))
    print(check("127.0.0.1", 9))
    # .invalid is reserved for names that are intentionally invalid.
    print(check("no-such-host.invalid", 80))
