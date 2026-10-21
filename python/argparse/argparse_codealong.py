# Command-line arguments are values supplied after a script's name.
# Example: python deploy.py v2 --dry-run
# sys and argparse are built into Python; no installation is needed.
# Run this file: python python/argparse/argparse_codealong.py

import argparse
import sys


def main():
    # 1. Understand sys.argv using a pretend argument list.
    # The real sys.argv contains the script name followed by its arguments.
    print("\n--- 1. Script name and arguments ---")
    argv = ["deploy.py", "v2", "--dry-run"]
    print(argv[0])   # deploy.py: the script name.
    print(argv[1:])  # ['v2', '--dry-run']: everything after the script name.
    print(f"Actual arguments for this file: {sys.argv}")

    # 2. Read the arguments manually.
    print("\n--- 2. Manual argument handling ---")
    if len(argv) < 2:
        # Check the length before reading argv[1] to avoid IndexError.
        print("usage: deploy.py VERSION [--dry-run]")
    else:
        version = argv[1]
        dry_run = "--dry-run" in argv  # True if this string is in the list.
        print(f"version={version} dry_run={dry_run}")

    # 3. Let argparse handle a positional argument.
    # A positional argument is identified by its position, such as v2.
    print("\n--- 3. Positional argument ---")
    parser = argparse.ArgumentParser(
        description="Deploy a release of flask-demo."
    )
    parser.add_argument("version", help="the release to deploy, e.g. v2")

    # The list simulates command-line arguments, WITHOUT the script name.
    # In a real CLI, parse_args() reads sys.argv[1:] automatically.
    args = parser.parse_args(["v2"])
    print(args.version)  # v2. Parsed values are accessed as attributes.

    # 4. Supply an optional argument with a default value.
    # --config is a named option followed by its value.
    print("\n--- 4. Default and custom config paths ---")
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    parser.add_argument(
        "--config", default="deploy.yaml", help="path to the config file"
    )
    print(parser.parse_args(["v2"]).config)  # deploy.yaml
    print(parser.parse_args(["v2", "--config", "staging.yaml"]).config)

    # 5. Require a named option.
    print("\n--- 5. Required environment ---")
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    parser.add_argument(
        "--env", required=True,
        help="environment to deploy to, e.g. staging",
    )
    print(parser.parse_args(["v2", "--env", "staging"]).env)

    # Missing --env prints an error to stderr and raises SystemExit.
    # Catch it here so we can continue to the remaining teaching examples.
    try:
        print(parser.parse_args(["v2"]).env)  # This print never runs.
    except SystemExit as error:
        print(f"Missing --env: argparse exited with code {error.code}")

    # 6. Convert an argument to a number.
    # Command-line input starts as text. type=int converts it to an integer.
    print("\n--- 6. Integer argument ---")
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8801)
    args = parser.parse_args(["--port", "9000"])
    print(args.port, type(args.port).__name__)  # 9000 int
    print(parser.parse_args([]).port)          # 8801: the default.

    # 7. Restrict a value to a set of choices.
    # Other values, such as xml, would cause a parsing error.
    print("\n--- 7. Allowed choices ---")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--format", choices=["text", "json", "csv"], default="text"
    )
    print(parser.parse_args(["--format", "json"]).format)  # json

    # 8. Make a boolean flag that does not need a following value.
    # store_true means False when absent and True when present.
    print("\n--- 8. Boolean flag ---")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run", action="store_true",
        help="validate and stop, change nothing",
    )
    # argparse changes the hyphen in --dry-run to an underscore in dry_run.
    print(parser.parse_args([]).dry_run)             # False
    print(parser.parse_args(["--dry-run"]).dry_run)  # True
    # Your program must use this value to implement dry-run behaviour.

    # 9. Display automatically generated help.
    print("\n--- 9. Help message ---")
    parser = argparse.ArgumentParser(
        description="Deploy a release of flask-demo."
    )
    parser.add_argument("version", help="the release to deploy")
    parser.add_argument("--config", default="deploy.yaml", help="config file path")
    parser.add_argument("--dry-run", action="store_true", help="change nothing")
    parser.print_help()
    # In a real CLI, -h or --help displays help and exits with code 0.
    # print_help() displays it without exiting.

    # 10. Handle invalid argument types.
    print("\n--- 10. Invalid port ---")
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int)
    try:
        parser.parse_args(["--port", "not-a-number"])
    except SystemExit as error:
        # argparse normally exits with code 2 for invalid arguments.
        print(f"argparse exited with code {error.code}")


# Run the examples only when executing this file directly.
if __name__ == "__main__":
    main()
