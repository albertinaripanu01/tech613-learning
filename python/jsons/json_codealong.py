import json
from pathlib import Path

# 1. Convert a JSON string into a Python dictionary.
text = '{"hostname": "web-01", "port": 8801}'
server = json.loads(text)

print("--- JSON string to dictionary ---")
print(server["hostname"])
print(type(server))

# 2. Convert a Python dictionary into a JSON string.
server = {"hostname": "web-01", "port": 8801}

print("\n--- Dictionary to JSON string ---")
print(json.dumps(server))
print(json.dumps(server, indent=2))

# Keep files beside this Python script.
HERE = Path(__file__).parent
inventory_file = HERE / "inventory.json"
report_file = HERE / "report.json"

# 3. Read inventory.json using Path and json.loads().
# Save your inventory JSON beside this script first.
if inventory_file.exists():
    print("\n--- Read inventory using json.loads ---")
    data = json.loads(inventory_file.read_text(encoding="utf-8"))
    print(data["site"])
    print(len(data["servers"]))

    # 4. Read the same file using json.load().
    print("\n--- Read inventory using json.load ---")
    with open(inventory_file, encoding="utf-8") as file:
        data = json.load(file)

    print(data["site"])
    print(data["servers"][0]["hostname"])
else:
    print("\nPlace inventory.json beside this script to run the inventory examples.")

# 5. Catch invalid JSON: trailing comma.
print("\n--- Invalid JSON: trailing comma ---")
try:
    json.loads('{"hostname": "web-01",}')
except json.JSONDecodeError as error:
    print(f"Could not parse: {error}")

# 6. Catch invalid JSON: missing comma.
print("\n--- Invalid JSON: missing comma ---")
try:
    json.loads('{"hostname": "web-01" "port": 8801}')
except json.JSONDecodeError as error:
    print(f"line {error.lineno}, column {error.colno}: {error.msg}")

# 7. Write a Python dictionary to report.json.
report = {
    "checked": 8,
    "healthy": 6,
    "problems": ["api-01", "api-01-stg"],
}

with open(report_file, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=2)

# 8. Read and display the saved report.
print("\n--- Saved report.json ---")
print(report_file.read_text(encoding="utf-8"))