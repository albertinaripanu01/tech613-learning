"""Lab solution - validate a deployment config.

Stage 1 of Friday's deployment automator. The shape of ConfigError here is the
shape in both starter repositories.
"""

from pathlib import Path

import yaml

HERE = Path(__file__).parent
GOOD = HERE / "deploy.yaml"
BROKEN = HERE / "deploy_broken.yaml"

REQUIRED_KEYS = (
    "app_name",
    "release_version",
    "releases_dir",
    "deploy_dir",
    "backup_dir",
    "app_port",
    "health_check_url",
    "health_check_retries",
    "health_check_delay_seconds",
)


class ConfigError(Exception):
    """Raised when the config cannot be used. Carries every problem found.

    Storing the list rather than one message is what lets the caller print all
    of them. Joining them for super().__init__ means str(error) is still useful
    if the caller does not know about .problems.
    """

    def __init__(self, problems):
        self.problems = list(problems)
        super().__init__("; ".join(self.problems))


def read_yaml(path):
    """Parse a YAML file."""
    with open(path, encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_config(path):
    """CORE - load the config, raising ConfigError rather than crashing.

    Note what is caught: the two things that genuinely happen to a config file,
    named individually. A bare `except Exception` here would also swallow a
    mistake in read_yaml, and we would never know.
    """
    try:
        config = read_yaml(path)
    except FileNotFoundError:
        raise ConfigError([f"config file not found: {path}"]) from None
    except PermissionError:
        raise ConfigError([f"config file not readable: {path}"]) from None
    except yaml.YAMLError as error:
        raise ConfigError([f"config file is not valid YAML: {error}"]) from None

    if not isinstance(config, dict):
        raise ConfigError([f"config file is not a mapping: {path}"])

    return config


def validate(config):
    """EXTENSION - check the config makes sense, reporting every problem."""
    problems = []

    for key in REQUIRED_KEYS:
        if key not in config:
            problems.append(f"missing key: {key}")

    port = config.get("app_port")
    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        problems.append(
            f"app_port must be an integer between 1 and 65535, got {port!r}"
        )

    retries = config.get("health_check_retries")
    if not isinstance(retries, int) or isinstance(retries, bool) or retries <= 0:
        problems.append(
            f"health_check_retries must be greater than 0, got {retries!r}"
        )

    url = config.get("health_check_url")
    if not isinstance(url, str) or not url.startswith("http"):
        problems.append(f"health_check_url must start with http, got {url!r}")

    if problems:
        raise ConfigError(problems)


if __name__ == "__main__":
    for path in (GOOD, BROKEN):
        print(f"--- {path.name} ---")
        try:
            config = load_config(path)
            validate(config)
        except ConfigError as error:
            for problem in error.problems:
                print(f"  {problem}")
        else:
            print("  config is valid")
