# PM2, Nginx reverse proxy and EC2 user data

## 1. Start the application

Commands retained from the existing draft:

```bash
cd app
pm2 start app.js
```

PM2 manages the Node.js application process. In this recording the trainer mentions PM2 but uses the following foreground alternative during the demonstration (around 16:17):

```bash
cd app
npm start
```

Use the appropriate startup method for the application; these are alternatives.

## 2. Reverse proxy concepts (00:12–11:01)

A proxy acts on behalf of another system. A forward proxy represents clients; a reverse proxy receives requests on behalf of servers. Reverse proxies can route requests to an application port, balance traffic across servers, terminate HTTPS, and cache responses.

For this exercise:

```text
Browser → HTTP port 80 → Nginx → localhost:3000 → Node.js app
```

The browser visits `http://<PUBLIC_IP>/` without adding `:3000`. Nginx forwards the request internally. This is proxying rather than a browser redirect.

## 3. Install and inspect Nginx 

Installation command retained from the draft (Nginx is already installed in the demo):

```bash
sudo apt install nginx
```

List the configuration directory, inspect its detailed listing, and locate the default site:

```bash
ls /etc/nginx
ls /etc/nginx -l
ls /etc/nginx/sites-available
```

`sites-available` contains the available site configurations. The demonstration edits `default`.

## 4. Configure the reverse proxy manually 

```bash
sudo nano /etc/nginx/sites-available/default
```

Inside the existing server block listening on port 80, find `location /`. Comment out or replace the original `try_files` line:

```nginx
location / {
    # try_files $uri $uri/ =404;
    proxy_pass http://localhost:3000/;
}
```

The trailing slash is visible in the demonstrated configuration. The destination is `localhost`, because the app runs on the same machine as Nginx.

In Nano, use **Ctrl+O**, then **Enter** to save, and **Ctrl+X** to exit.

<img width="820" height="506" alt="image" src="https://github.com/user-attachments/assets/fc7495bc-dc44-4453-a9a6-d2bba7a0be83" />


## 5. Restart Nginx and run the app (15:40–17:09)

```bash
sudo systemctl restart nginx
cd app
npm start
```

The demonstration then opens the server public IP in a browser without a port suffix and reaches the app. The app must be running for Nginx to forward requests successfully.

<img width="846" height="577" alt="image" src="https://github.com/user-attachments/assets/a4d02b66-d5d7-4397-a162-8a1de6781c16" />


## 6. Automate the edit with sed (17:13–25:13)

Nano is interactive, so use `sed` in a provisioning script. The trainer inspects its help:

```bash
sed --help
```

The replacement demonstrated with slash delimiters is transcribed as:

```bash
sudo sed -i "s/try_files \$uri \$uri\/ =404;/proxy_pass http:\/\/localhost:3000\/;/" /etc/nginx/sites-available/default
```

- `-i` edits the file in place.
- `s/old/new/` replaces matching text.
- With double quotes, `\$` protects the literal dollar sign from shell expansion.
- `\/` escapes slashes used inside a slash-delimited expression.

At 24:00–25:11:

```bash
sudo sed -i 's|try_files $uri $uri/ =404;|proxy_pass http://localhost:3000/;|' /etc/nginx/sites-available/default
```

Use one replacement approach. These expressions expect the original text to match; inspect the file if nothing changes. If the old line was already commented out during the manual exercise, start from the original configuration when testing the automated replacement.

<img width="1183" height="607" alt="image" src="https://github.com/user-attachments/assets/80672826-e812-47c0-8468-e4736dda3f18" />


Other commands discussed, rather than demonstrated with a specific filename (18:15–18:50):

```bash
cat <file>
touch <file>
```

`cat` displays file contents; `touch` creates a missing file or updates an existing file timestamp.

## 7. Run provisioning through EC2 user data (25:26–34:25)

1. Open the EC2 **Launch an instance** wizard.
2. Configure the usual instance options; the recording uses Ubuntu 24.
3. Expand **Advanced details**.
4. Scroll to **User data** at the bottom.
5. Paste the working provisioning Bash script (the UI also allows a file upload).
6. Begin the script with its interpreter declaration:

```bash
#!/bin/bash
```

The script should retrieve the app code, install its dependencies, configure Nginx as a reverse proxy, and start the application. The recording does not supply a complete provisioning script or a repository URL here, so those missing commands are not invented in these notes.

The goal is a fresh instance that deploys the app at first boot and serves it at its public IP without manual SSH setup. Document fixes needed to make the script repeatable. Amazon Machine Images are mentioned as the next topic (34:40–35:18).

## Clarifications

- The transcript says “port 82” once; the demonstrated listener and explanation use **port 80**.
- Base64 is **encoding, not encryption**. Encoding user data does not make secrets confidential.
- TLS termination does not itself encrypt traffic between the proxy and its backend.
- The draft PM2 command is retained, but this recording does not demonstrate PM2 installation, reboot persistence, or a full PM2 setup.
