"""Practice Python collections using hosts, servers, and inventory data."""

# 1. Lists store multiple values in order. Indexes start at zero.
hosts = ["web-01", "web-02", "api-01"]

print(hosts[0])   # web-01: index 0 selects the first item.
print(hosts[-1])  # api-01: negative indexes count backwards from the end.
print(len(hosts)) # 3: len() returns the number of items.

# 2. Lists are mutable, so we can add and remove items after creating them.
hosts = ["web-01", "web-02"]
hosts.append("api-01")  # Add a new item to the end of the list.
hosts.remove("web-01")  # Remove the first matching value (not an index).
print(hosts)           # ['web-02', 'api-01']
# remove() raises ValueError if the value is not in the list.

# 3. A for loop visits each item in a collection in order.
# The variable host holds the current item during each iteration.
# An f-string inserts the value of host into the message.
for host in ["web-01", "web-02", "api-01"]:
    print(f"Checking {host}")
# Output: Checking web-01, Checking web-02, Checking api-01 (one per line).

# 4. Tuples are ordered collections whose items cannot be replaced or removed.
# Unpacking assigns each tuple item to a separate variable.
server = ("web-01", 8801)
hostname, port = server  # Two variables match the two items in this tuple.
print(f"{hostname} on {port}")  # web-01 on 8801

# 5. Dictionaries store key-value pairs, giving each value a descriptive name.
server = {
    "hostname": "web-01",
    "environment": "production",
    "port": 8801,
    "disk_used": 41,
}

print(server["hostname"])  # web-01: look up a value using its key.
print(server["port"])      # 8801
# Using square brackets with a missing key raises KeyError.

# 6. get() safely looks up a key that might be missing.
server = {"hostname": "web-01"}
print(server.get("port"))        # None: the key is missing, with no default.
print(server.get("port", 8801))  # 8801: return this default if the key is missing.
# get() does not add the missing key or its default to the dictionary.

# 7. items() lets us loop over both the keys and their values.
server = {"hostname": "web-01", "port": 8801, "disk_used": 41}

for key, value in server.items():
    print(f"{key}: {value}")
# Each pair is unpacked into key and value, printing one pair per line.

# 8. A list of dictionaries can represent an inventory of servers.
# Each list item is a dictionary describing one server.
inventory = [
    {"hostname": "web-01", "environment": "production", "bytes": 8419203},
    {"hostname": "api-01", "environment": "production", "bytes": 15220477},
    {"hostname": "web-01-stg", "environment": "staging", "bytes": 402117},
]

print(inventory[0]["hostname"])  # web-01
# First select the dictionary at index 0, then look up its hostname key.

# 9. Collections can be nested: this dictionary contains a list of dictionaries.
config = {
    "site": "eu-west",
    "servers": [
        {"hostname": "web-01", "port": 8801},
        {"hostname": "api-01", "port": 8802},
    ],
}

print(config["servers"][0]["port"])  # 8801
# Follow the structure: servers key -> first list item -> port key.

# 10. Another inventory example, storing a hostname and byte count per server.
# This assignment replaces the earlier inventory value.
inventory = [
    {"hostname": "web-01", "bytes": 8419203},
    {"hostname": "api-01", "bytes": 15220477},
    {"hostname": "db-01", "bytes": 2044118},
]
# The bytes values are integers, so they can be used in calculations later.
