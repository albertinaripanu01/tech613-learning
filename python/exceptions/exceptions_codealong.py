import json
from pathlib import Path

# An exception is an error that interrupts normal execution.
# "try" runs code that might fail.
# "except" handles a particular error so the program can continue.

# 1. Catch a ValueError.
print("\n--- 1. Catch an invalid number ---")

try:
    # This fails because "not-a-port" cannot become an integer.
    port = int("not-a-port")
except ValueError:
    print("That is not a number")


# 2. Store the exception in a variable.
print("\n--- 2. Display the error details ---")

try:
    port = int("not-a-port")
except ValueError as error:
    # "error" contains the exception that Python raised.
    print(f"Could not read the port: {error}")


# 3. Catch invalid JSON.
print("\n--- 3. Catch invalid JSON ---")

try:
    config = json.loads("{broken")
except json.JSONDecodeError as error:
    print(f"Config is not valid JSON: {error}")


# 4. A successful operation does not run the except block.
print("\n--- 4. Successful conversion ---")

try:
    value = int("8801")
except ValueError:
    # Catch the specific error you expect.
    # "except Exception" would catch many different errors,
    # which can accidentally hide unrelated programming mistakes.
    value = None

print(f"value is {value}")


# 5. Common exceptions.md.
#
# FileNotFoundError: a file or folder you need cannot be found.
# PermissionError: an operation is blocked by access permissions.
# json.JSONDecodeError: the text is not valid JSON.
# KeyError: a dictionary does not contain the requested key.
# ValueError: a value is unsuitable, such as int("abc").
# TypeError: an operation receives an unsuitable type, such as "8801" + 1.


# 6. Catch more than one exception type with the same handler.
print("\n--- 6. Handle multiple exception types ---")

try:
    # "raise" deliberately creates an exception.
    # Here it simulates a permission problem for demonstration.
    raise PermissionError("denied")
except (FileNotFoundError, PermissionError) as error:
    print(f"Cannot read the config: {error}")


# 7. Use else and finally.
print("\n--- 7. try, except, else and finally ---")

try:
    port = int("8801")
except ValueError:
    # Runs if the conversion raises ValueError.
    print("Bad port")
else:
    # Runs only if the try block finishes without an exception.
    print(f"Port is {port}")
finally:
    # Runs whether the conversion succeeds or fails.
    print("Checked the port")


# 8. Use finally to close a file.
print("\n--- 8. Close a file with finally ---")


def read_config(path):
    # If opening fails, there is no open file to close.
    file = open(path, encoding="utf-8")

    try:
        return file.read()
    finally:
        # Runs before the function returns, even if reading fails.
        file.close()
        print("File closed")


# Look for app.log beside this Python script.
log_path = Path(__file__).parent / "app.log"

try:
    text = read_config(log_path)
    print(f"The file contains {len(text)} characters")
except (FileNotFoundError, PermissionError) as error:
    print(f"Could not open app.log: {error}")

# In everyday code, "with open(...)" automatically handles closing:
#
# with open(log_path, encoding="utf-8") as file:
#     text = file.read()


# 9. Raise an exception when a value breaks your rules.
print("\n--- 9. Validate a port ---")


def check_port(port):
    # This function expects an integer.
    # Valid ports are between 1 and 65535, including both endpoints.
    if not 1 <= port <= 65535:
        raise ValueError(f"Port {port} is out of range")

    return port


print(check_port(8801))

try:
    check_port(70000)
except ValueError as error:
    print(f"Invalid port: {error}")


# 10. Define your own exception type.
print("\n--- 10. A custom exception ---")


class ConfigError(Exception):
    """The configuration file is missing or wrong."""


# Inheriting from Exception makes ConfigError an exception type.
# Its name lets us handle configuration problems specifically.
try:
    raise ConfigError("deploy.yaml not found")
except ConfigError as error:
    print(f"Config problem: {error}")


# 11. Store several problems in a custom exception.
print("\n--- 11. Report all configuration problems ---")


class ConfigValidationError(Exception):
    """Raised when required configuration keys are missing."""

    def __init__(self, problems):
        # __init__ runs when we create this exception.
        # Save the list so the except block can access each problem.
        self.problems = problems

        # Join the problems into one message.
        # super().__init__ passes that message to Exception.
        super().__init__("; ".join(problems))


def validate(config):
    problems = []

    # Check every required key before deciding whether to raise.
    for key in ("app_name", "release_version", "app_port"):
        if key not in config:
            problems.append(f"Missing key: {key}")

    # A non-empty list means at least one problem was found.
    if problems:
        raise ConfigValidationError(problems)


try:
    # This dictionary is missing release_version and app_port.
    validate({"app_name": "flask-demo"})
except ConfigValidationError as error:
    print(f"{len(error.problems)} problems found")

    for problem in error.problems:
        print(f"  - {problem}")
else:
    print("Configuration passed validation")