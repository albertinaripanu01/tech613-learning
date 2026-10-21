from pathlib import Path
print("Create a new file called app.log and writes whatever is in the array inside it")
lines = ["web-01 OK", "api-01 DEGRADED"]
with open("report.txt", "w", encoding="utf-8") as file:
    for line in lines:
        file.write(f"{line}\n")
print(Path("report.txt").read_text(encoding="utf-8"))
print("----------------------------------")


log_file = Path("app.log")
print(log_file.exists())
print(log_file.name)
print(log_file.suffix)

print("```````````````````````````````````")
print("Create a variable contains the path")
config = Path("configs") / "targets.yaml"
print(config)

print("----------------------------------")
print("text variable gets everything that is inside the file as a string")
file = open("app.log", encoding="utf-8")
text = file.read()
file.close()

print("```````````````````````````````````")
print("printing the lentgth of text inside the file")
with open("app.log", encoding="utf-8") as file:
    text = file.read()
print(len(text))

print("----------------------------------")
print("read through the file looking for the word error, and prints online the lines containing the error")
with open("app.log", encoding="utf-8") as file:
    for line in file:
        if "ERROR" in line:
            print(line.rstrip())
