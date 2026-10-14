"""Lab - read a server inventory.

This is the same eight-server inventory used throughout the week. On Day 2 you
will load it from a JSON file instead of typing it; the shape will be identical.

Run  python3 check_inventory.py  to test your answers.
"""

SERVERS = [
    {"hostname": "web-01", "ip_address": "10.24.1.11", "environment": "production",
     "role": "web", "port": 8801, "status": "healthy",
     "disk_percent_used": 41, "bytes_transferred": 8419203},
    {"hostname": "web-02", "ip_address": "10.24.1.12", "environment": "production",
     "role": "web", "port": 8801, "status": "healthy",
     "disk_percent_used": 38, "bytes_transferred": 7733910},
    {"hostname": "api-01", "ip_address": "10.24.2.21", "environment": "production",
     "role": "api", "port": 8802, "status": "degraded",
     "disk_percent_used": 88, "bytes_transferred": 15220477},
    {"hostname": "api-02", "ip_address": "10.24.2.22", "environment": "production",
     "role": "api", "port": 8802, "status": "healthy",
     "disk_percent_used": 52, "bytes_transferred": 14098320},
    {"hostname": "db-01", "ip_address": "10.24.3.31", "environment": "production",
     "role": "database", "port": 5432, "status": "healthy",
     "disk_percent_used": 73, "bytes_transferred": 2044118},
    {"hostname": "web-01-stg", "ip_address": "10.30.1.11", "environment": "staging",
     "role": "web", "port": 8801, "status": "healthy",
     "disk_percent_used": 19, "bytes_transferred": 402117},
    {"hostname": "api-01-stg", "ip_address": "10.30.2.21", "environment": "staging",
     "role": "api", "port": 8802, "status": "down",
     "disk_percent_used": 22, "bytes_transferred": 0},
    {"hostname": "build-01", "ip_address": "10.40.9.91", "environment": "tooling",
     "role": "ci", "port": 8803, "status": "healthy",
     "disk_percent_used": 94, "bytes_transferred": 630885},
]


def list_servers(server):
    for item in server:
        # item is one dictionary
        print(item["hostname"], item["port"])



def count_production(server):
    # TODO: count the servers whose environment is "production"
    count=0
    for item in server:
        if item["environment"] == "production":
            count=count+1
    return count


def total_bytes(server):
    # TODO: add up bytes_transferred
    sumi=0
    for item in server:
        sumi=item["bytes_transferred"]+sumi
    return sumi


def busiest_host(server):

    # TODO: find the server with the largest bytes_transferred
    max_bytes = 0
    busiest_server = {}
    for item in server:
        if item["bytes_transferred"] > max_bytes:
            max_bytes = item["bytes_transferred"]
            busiest_server = item
    if max_bytes == 0:
        return "everything is 0"
    else:
        return busiest_server["hostname"]


if __name__ == "__main__":
    list_servers(SERVERS)
    print(f"production servers: {count_production(SERVERS)}")
    print(f"total bytes: {total_bytes(SERVERS)}")
    print(f"busiest: {busiest_host(SERVERS)}")
