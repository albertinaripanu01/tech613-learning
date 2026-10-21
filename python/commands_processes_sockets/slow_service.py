"""A tiny service to start, check and stop. You do not need to change this.

It takes a few hundred milliseconds to begin listening, which is deliberate:
a service is not ready the instant the process starts, and code that assumes it
is will fail intermittently. That is the most annoying kind of bug, so it is
worth meeting on purpose.

    python3 slow_service.py [port] [startup_delay_seconds]
"""

import socket
import sys
import time

DEFAULT_PORT = 8801
DEFAULT_DELAY = 0.4


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    delay = float(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_DELAY

    # The service is "booting". Nothing is listening yet.
    time.sleep(delay)

    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", port))
    server.listen(5)

    # Unbuffered so a parent process reading our output sees this immediately.
    print(f"listening on 127.0.0.1:{port}", flush=True)

    try:
        while True:
            connection, _ = server.accept()
            connection.sendall(b"ok\n")
            connection.close()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()


if __name__ == "__main__":
    main()
