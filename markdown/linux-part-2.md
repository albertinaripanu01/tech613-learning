# Linux Part 2

## Install Nginx on Ubuntu 24.04

Save this script as `install-nginx.sh`. Each comment and command goes on its own line.

```bash
#!/bin/bash

# Purpose: install Nginx on a fresh Ubuntu 24.04 system
set -e

# Update the package list
sudo apt-get update

# Upgrade installed packages
sudo apt-get upgrade -y

# Install Nginx
sudo apt-get install nginx -y

# Check the configuration before restarting
sudo nginx -t

# Restart Nginx, including after configuration changes
sudo systemctl restart nginx

# Enable Nginx to start at boot
sudo systemctl enable nginx
```

Run the script and check the service:

```bash
bash install-nginx.sh
systemctl status nginx
```

`set -e` stops this script if a command fails. `-y` automatically confirms package changes. `enable` configures startup at boot; `restart` restarts the service now.

See [Ubuntu: install Nginx](https://ubuntu.com/server/docs/how-to-install-nginx/) for installation and service checks.

## Process commands

A process is a running program. Its **PID** is its process ID. A background job is tracked by the shell that started it.

| Command | Purpose |
| --- | --- |
| `ps --help simple` | Show basic help for `ps` |
| `ps` | Show processes selected by default, usually those for your user on the current terminal |
| `ps -A` | Show all processes |
| `ps aux` | Show processes for all users, with CPU and memory information |
| `ps -ef` | Show all processes in full format, including PID and parent PID |
| `top` | Monitor processes interactively; press `q` to quit |
| `htop` | Monitor processes interactively with an easier navigation interface; press `q` to quit |
| `sleep 3` | Wait for 3 seconds in the foreground |
| `sleep 5000` | Wait for 5000 seconds in the foreground |
| `Ctrl+C` | Send an interrupt to the foreground process group; usually stops a running command |
| `sleep 6000 &` | Start a 6000-second sleep in the background |
| `jobs` | Show jobs started in the current shell |
| `jobs -l` | Show the current shell's jobs and their PIDs |
| `kill PID` | Send SIGTERM to request that a process stops |
| `kill -1 PID` | Send SIGHUP; terminates `sleep`, while some other programs handle it differently |
| `kill -9 PID` | Send SIGKILL to force a process to stop immediately |

If `htop` is not installed on Ubuntu, install it with `sudo apt-get install htop`.

## Practice: foreground and background processes

### 1. Stop a foreground command

```bash
sleep 3
sleep 5000
```

The first command finishes after 3 seconds. While the second is running, press **Ctrl+C** to interrupt it and return to the prompt.

### 2. Start a background process

```bash
sleep 6000 &
jobs -l
ps
```

The `&` returns you to the prompt while the command runs. `jobs -l` shows a job number, PID, status, and command. Use the PID belonging to your `sleep 6000` process:

```bash
# Replace PID with the actual process ID before running
kill -1 PID
jobs
```

### 3. Start two more processes and stop them

```bash
sleep 7000 &
sleep 8000 &
jobs -l
ps
```

Find the PID of each sleep process. Stop the first with SIGTERM and the second with SIGKILL:

```bash
# Replace FIRST_PID with the PID of sleep 7000
kill FIRST_PID
jobs

# Replace SECOND_PID with the PID of sleep 8000
kill -9 SECOND_PID
jobs
```

Use your own PIDs, rather than numbers from someone else's terminal. A **job number** such as `[1]` is different from a PID. Bash can also target a job with `kill %1`.

`jobs` may report **Terminated**, **Hangup**, or **Killed** once; a later check may omit the completed job. Try SIGTERM first for normal use. SIGKILL prevents a program from cleaning up. See the [kill manual](https://man7.org/linux/man-pages/man1/kill.1.html) for signal details.
