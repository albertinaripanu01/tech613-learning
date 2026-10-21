"""Lab - give Tuesday's config loader a command line.

load_config.py is the working version from Tuesday. You are not changing it;
you are wrapping it in a tool somebody else could run.

    python3 cli.py
    python3 cli.py --config deploy_broken.yaml
    python3 cli.py --dry-run

Run  python3 check_cli.py  to test.
"""

import argparse
import sys

from load_config import ConfigError, load_config, validate

EXIT_OK = 0
EXIT_CONFIG = 1


def build_parser():
    """CORE - build and return the ArgumentParser.

    Arguments to add:

        --config    path to the config file, default "deploy.yaml"
        --dry-run   a flag: validate and stop, change nothing

    EXTENSION adds:
        --format    choices "text" and "json", default "text"

    STRETCH adds:
        --verbose   a flag, for the logging level

    Give every argument a help= string. It is the documentation somebody reads
    at 3am and it cannot go out of date.

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Validate a deployment config.",
    )
    # TODO
    return parser


def main(argv=None):
    """CORE - parse arguments, validate the config, return an exit code.

    Exit codes, from Friday's contract:

        0   the config is valid
        1   the config is invalid, nothing was touched

    Print what you found either way. On --dry-run, say clearly that nothing
    would be changed.

    Args:
        argv: list of arguments, or None to read the real command line

    Returns:
        int exit code
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    # TODO
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
