## Nginx commands (Ubuntu 24.04)

| Command | Purpose |
| --- | --- |
| `sudo apt-get update` | Update the package list |
| `sudo apt-get upgrade -y` | Upgrade installed packages and automatically confirm |
| `sudo apt-get install nginx -y` | Install Nginx and automatically confirm |
| `sudo nginx -t` | Check the Nginx configuration for errors |
| `sudo systemctl restart nginx` | Restart Nginx after configuration changes |
| `sudo systemctl enable nginx` | Enable Nginx to start at boot |
| `systemctl status nginx` | Check the Nginx service status |

## Process commands

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
