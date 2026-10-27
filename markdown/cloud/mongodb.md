## Create an AWS EC2 Instance for MongoDB

### 1. Name and tags

- **Name:** `tech613-albertina-mongodb`

### 2. Application and OS image

- **Operating system:** Ubuntu
- **Version:** Ubuntu Server 24.04 LTS

### 3. Key pair

- **Key pair:** `tech613-albertina-aws-key`

### 4. Network settings

Select **Create security group** and enter:

- **Security group name:** `tech613-albertina-mongodb-sg`
- **Description:** `SG for mongodb connections`

Click **Add security group rule** to add the MongoDB rule:

| Type | Protocol | Port | Source |
|---|---|---|---|
| SSH | TCP | 22 | My IP |
| Custom TCP | TCP | 27017 | My IP |

> **My IP** limits access to your current public IP address (`/32`).

![Security group configuration](https://github.com/user-attachments/assets/315f0e1c-a166-4272-a6da-81dfe8ce9f40)

### 5. Launch the instance

Review the settings and click **Launch instance**.

Once the instance is running, copy its **Public IPv4 address** for SSH and MongoDB Compass connections.

> **Compatibility note:** The earlier MongoDB installation commands use the Ubuntu 22.04 (`jammy`) repository. They should not be used unchanged for this Ubuntu 24.04 instance.

# Install MongoDB 7.0.22 on Ubuntu

> These commands use the MongoDB repository for Ubuntu 22.04 (Jammy).

## 1. Check your location and update Ubuntu

```bash
ls
pwd
sudo apt update -y
sudo apt upgrade -y
```

## 2. Import the MongoDB signing key

```bash
curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-7.0.gpg \
  --dearmor
```

## 3. Add the MongoDB repository

```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
```

Update the package list:

```bash
sudo apt update -y
```

## 4. Install MongoDB

```bash
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  mongodb-org=7.0.22 \
  mongodb-org-database=7.0.22 \
  mongodb-org-server=7.0.22 \
  mongodb-mongosh \
  mongodb-org-shell=7.0.22 \
  mongodb-org-mongos=7.0.22 \
  mongodb-org-tools=7.0.22 \
  mongodb-org-database-tools-extra=7.0.22
```

Check the service:

```bash
sudo systemctl status mongod
```

Press `q` to leave the status screen.

![MongoDB service status](https://github.com/user-attachments/assets/28b97a59-81bf-48dc-8733-694053ed490d)

## 5. Edit the MongoDB configuration

```bash
cd /etc
sudo nano mongod.conf
```

Change the **bind address**, not the port, from `127.0.0.1` to `0.0.0.0`:

```yaml
net:
  port: 27017
  bindIp: 0.0.0.0
```

> `0.0.0.0` makes MongoDB listen on all IPv4 network interfaces. Restrict AWS inbound port **27017** to your own public IP (`/32`), and enable MongoDB authentication before allowing remote access.

Save with **Ctrl+O**, press **Enter**, then exit with **Ctrl+X**.

![MongoDB network configuration](https://github.com/user-attachments/assets/35a44047-b4ac-41fd-a5b5-f55b1df5de96)

Read the saved configuration:

```bash
cat /etc/mongod.conf
```

## 6. Start MongoDB and enable it on boot

Return to your home folder:

```bash
cd ~
pwd
```

The expected location is `/home/ubuntu`.

Restart MongoDB to apply the configuration, then enable it on boot:

```bash
sudo systemctl restart mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```

Press `q` to leave the status screen.

![MongoDB running](https://github.com/user-attachments/assets/c8917fba-bf76-4d0b-b1c2-b820a7068d61)

## 7. Connect using MongoDB Compass

Open **MongoDB Compass**, create a new connection, and enter your instance’s public IP:

```text
mongodb://PUBLIC_IP:27017
```

Replace `PUBLIC_IP` with your instance’s **Public IPv4 address**. If authentication is enabled, enter your database username, password, and authentication database in Compass.

![MongoDB Compass connection](https://github.com/user-attachments/assets/34b8418d-2b4d-4eb1-b387-e582190cb8cf)

## 8. Create a database

Select the **Create database** button.

![Database toolbar](https://github.com/user-attachments/assets/a334f6d8-b41a-41e7-92ac-be84db16f573)

Enter a **database name** and an initial **collection name**, then click **Create Database**.

![Create a database](https://github.com/user-attachments/assets/4cd0336e-3fd7-4c47-9634-8b7bb2d98ed6)
