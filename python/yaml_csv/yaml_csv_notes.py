# YAML stores settings using names, values, lists, and indentation.
# CSV stores tables using rows and columns separated by commas.
# Install PyYAML if needed: python -m pip install pyyaml
# Run from the repository root: python python/yaml_csv/yaml_csv_notes.py

import csv
from pathlib import Path

import yaml

# Find this script's folder, even when you run it from another directory.
HERE = Path(__file__).parent
# These examples create or overwrite config.yaml and servers.csv in this folder.


# 1. Read YAML from a string.
# YAML stands for YAML Ain't Markup Language.
# Indentation groups related data. Use spaces.
# The dash starts an item in the servers list.
text = """
site: eu-west
servers:
  - hostname: web-01
    port: 8801
"""

# safe_load converts YAML into Python dictionaries, lists, and other values.
config = yaml.safe_load(text)

print(config["site"])                # eu-west
# [0] selects the first server; ["port"] gets its port.
print(config["servers"][0]["port"])  # 8801
print(type(config))                 # <class 'dict'>


# 2. Write YAML text to a file, then read it back.
# \n starts a new line in the text.
text = "site: eu-west\nport: 8801\n"

# "w" writes to a file, replacing any existing contents.
# UTF-8 tells Python how to encode and decode the text.
# The with block automatically closes the file, even if an error occurs.
with open(HERE / "config.yaml", "w", encoding="utf-8") as file:
    file.write(text)

with open(HERE / "config.yaml", encoding="utf-8") as file:
    config = yaml.safe_load(file)

print(config)  # {'site': 'eu-west', 'port': 8801}


# 3. Turn a Python dictionary into YAML.
config = {"site": "eu-west", "port": 8801}

# safe_dump returns YAML text. Passing a file writes that text to the file.
print(yaml.safe_dump(config))

with open(HERE / "config.yaml", "w", encoding="utf-8") as file:
    yaml.safe_dump(config, file)


# 4. Notice how PyYAML interprets unquoted values.
# These conversions describe PyYAML's default safe loader.
text = """
a: yes
b: no
c: true
d: on
e: off
region: NO
version: 1.20
mode: 0755
time: 12:30
"""

config = yaml.safe_load(text)

# repr shows quotes around strings, helping distinguish text from numbers.
for name, value in config.items():
    print(f"{name}: {value!r} ({type(value).__name__})")

# yes, true, and on become True; no, off, and NO become False.
# 1.20 becomes the float 1.2: numbers do not preserve trailing zeros.
# 0755 becomes the integer 493 because it is interpreted as octal (base 8).
# 12:30 becomes the integer 750: interpreted as base 60, it means 12 * 60 + 30.


# 5. Quote values that should stay as text.
text = """
app: flask-demo
version: "1.10"
debug: false
region: "NO"
mode: "0755"
time: "12:30"
"""

config = yaml.safe_load(text)
print(config)
# version, region, mode, and time now stay as strings.
# debug stays a boolean because false is deliberately unquoted.


# 6. Create and read a CSV file.
# CSV means Comma-Separated Values, like a spreadsheet saved as text.
# The first row gives the column names. Each remaining row is one server.
# Python includes the csv module; there is nothing extra to install for CSV.
with open(HERE / "servers.csv", "w", newline="", encoding="utf-8") as file:
    file.write(
        "hostname,environment,port\n"
        "web-01,production,8801\n"
        "web-02,development,8802\n"
    )

# newline="" lets the csv module handle line endings correctly.
with open(HERE / "servers.csv", newline="", encoding="utf-8") as file:
    # DictReader uses the header names as dictionary keys for each row.
    reader = csv.DictReader(file)

    for server in reader:
        # First row: {"hostname": "web-01", "environment": "production", "port": "8801"}
        print(server["hostname"])
        print(server["port"])

        # CSV reads these values as strings. int converts the port to a number
        # so we can do arithmetic with it.
        port = int(server["port"])
        print(port + 1)
