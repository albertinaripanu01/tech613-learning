hostname = "web-01"
port = 8801
disk_used_percent = 41.5
is_healthy = True

print(type(hostname))
print(type(port))
print(type(disk_used_percent))
print(type(is_healthy))

total_checks = 8
failed_checks = 2

passed = total_checks-failed_checks