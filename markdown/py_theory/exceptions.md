| Exception | What it means | Easy example |
|---|---|---|
| `ValueError` | You used the right kind of input, but its value cannot be used. | `int("hello")` — Python cannot turn the word `"hello"` into a whole number. |
| `json.JSONDecodeError` | You tried to read text as JSON, but its format is incorrect. | `json.loads('{"name": "Alex"')` — the closing `}` is missing. |
| `FileNotFoundError` | You tried to open a file that does not exist. | `open("missing.txt")` — there is no file called `missing.txt` at that location. |
| `PermissionError` | You tried to do something you do not have permission to do. | Trying to save changes to a file when your account only has permission to read it. |
| `KeyError` | You asked a dictionary for a key it does not contain. | `person = {"name": "Alex"}` followed by `person["age"]` — there is no `"age"` key. |
| `TypeError` | You tried to use a type of data that the operation does not support. | `"hello" + 5` — Python cannot directly add a string and a number. |
| `Exception` | A general parent class for most errors. Catching it handles many different error types. | `try: int("hello")` followed by `except Exception: print("Something went wrong")` — this catches the `ValueError`. |
| `ConfigError` *(custom)* | An error defined in this script to report a configuration problem. | `raise ConfigError("Settings file is missing")` — deliberately reports that the app cannot find its settings. |
| `ConfigValidationError` *(custom)* | An error defined in this script to report several missing settings together. | The settings contain only `app_name`, so the error reports that `release_version` and `app_port` are missing. |