# Create an EC2 Image for the Tic Tac Toe App

## 1. Create an Instance

Use the following settings:

- **Name:** `tech613-albertina-app-from-image`
- **Operating system:** Ubuntu
- **Version:** Ubuntu 24.04
- **Key pair:** `tech613-albertina-aws-key`

Connect to the new instance using Git Bash.

## 2. Create the Provisioning Script

Open a new script:

```bash
sudo nano prov-app.sh
```

Paste the following into `prov-app.sh`:

```bash
#!/bin/bash

echo "Update the sources list..."
sudo apt-get update -y
echo "Done!"

echo "Upgrade any packages available..."
sudo apt-get upgrade -y
echo "Done!"

echo "Install nginx..."
sudo apt-get install nginx -y
echo "Done!"

echo "Set up nginx reverse proxy..."
sudo apt install sed -y

# Escape the $ and / characters with a backslash.
sudo sed -i "s/try_files \$uri \$uri\/ =404;/proxy_pass http:\/\/localhost:3000\/;/" /etc/nginx/sites-available/default

# Restart nginx to activate the reverse proxy.
sudo systemctl restart nginx
echo "Done!"

# Uncomment if Git needs to be installed.
#echo "Install Git..."
#sudo apt-get install git -y
#echo "Done!"

echo "Install Node.js v20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && \
sudo apt-get install -y nodejs
echo "Install Node.js - Done!"

echo "Check Node.js version..."
node -v
echo "Done!"

# Choose ONE of the following application modes.

# OPTION 1: Client-local stateful
# Do not set STATEFUL_MODE or MONGODB_URI.
#echo "Using mode: Client-local stateful..."
#echo "Not setting STATEFUL_MODE or MONGODB_URI."
#echo "Done!"

# OPTION 2: Server-side stateful
#echo "Using mode: Server-side stateful..."
#echo "Setting STATEFUL_MODE=server..."
#export STATEFUL_MODE=server
#echo "Done!"

# OPTION 3: Persistent with MongoDB
# Only use this option if MongoDB is available.
# Ensure the security group permits the required MongoDB connection.
# Replace the IP address with your MongoDB instance's IP address.
#echo "Using mode: Persistent with MongoDB..."
#echo "Setting MONGODB_URI..."
#export MONGODB_URI=mongodb://172.31.19.159:27017/tictactoe
#echo "Done!"

echo "Clone the repository into a folder called repo..."
git clone https://github.com/LSF970/tech613-tictactoe-app.git repo
echo "Done!"

echo "Change to the app folder..."
cd repo
cd app
echo "Done!"

echo "Run npm install after the database VM has finished provisioning..."

# Installation attempts to seed the scoreboard.
# With OPTION 3, MongoDB must be running and accessible.
# With OPTION 2, seeding requires a running app instance.
npm install
echo "Done!"

# Uncomment to clear and seed the database manually.
# OPTION 1: Seeding is unavailable because the scoreboard is stored locally.
# OPTION 2: The app must be running.
# OPTION 3: MongoDB must be running and accessible.
#echo "Clearing and seeding the database..."
#node seeds/seed.js
#echo "Done!"

# Ways to start the app:

# 1. Start directly:
#node index.js
# Alternatively:
#npm start

# 2. Start in the background using forever or PM2.

# Using forever:
#sudo npm install forever -g
#forever stopall
#forever start index.js

# Using PM2:
echo "Install PM2..."
sudo npm install pm2 -g
echo "Done!"

echo "Stop existing PM2 processes..."
pm2 kill
echo "Done!"

echo "Start the app in the background with PM2..."
pm2 start index.js --name tic
echo "Done!"
```

Save the file and exit Nano.

## 3. Run the Provisioning Script

Check your current directory:

```bash
pwd
```

You should be in:

```text
/home/ubuntu
```

Run the script:

```bash
bash prov-app.sh
```

## 4. Check the nginx Configuration

Go to the root directory:

```bash
cd /
pwd
ls
```

The working directory should be `/`.

![Root directory contents](https://github.com/user-attachments/assets/6c67eb89-dd61-4d72-bbd0-5dbd83fa4000)

Navigate to the nginx configuration:

```bash
cd etc/
ls
```

Check that `nginx` is listed, then run:

```bash
cd nginx
ls
```

Check that `sites-available` is listed, then run:

```bash
cd sites-available
ls
```

You should see `default`.

Open the configuration file:

```bash
sudo nano default
```

Check the reverse proxy configuration, then exit Nano.

Open the app instance's public IP address in your browser and check that Tic Tac Toe works.

## 5. Create an Image

1. Stop the instance.
2. Select **Actions → Image and templates → Create image**.
3. Enter the following details:
   - **Name:** `tech613-albertina-image`
   - **Description:** `tic tac toe image`
   - **Tags:** Select the option to tag the image and snapshots together.
4. Create the image.

A result similar to the following should appear:

![Image creation result](https://github.com/user-attachments/assets/4777a664-d09a-482a-8043-e9a2ecd927cb)

Click the **AMI link**.

## 6. Launch an Instance from the Image

1. Select **Launch instance**.
2. Set the name to `tech613-albertina-app-from-image`.
3. Under **My AMIs → Owned by me**, select your image.
4. Under **Network settings**, choose **Select existing security group** and select your security group.
5. Launch the instance.

## 7. Connect to the New Instance

Open another Git Bash window and connect to the new instance.

For this Ubuntu image, use `ubuntu` as the SSH username. If the copied command uses `root`, replace it with `ubuntu`.

![SSH username reference](https://github.com/user-attachments/assets/4819e183-6224-4913-8cc4-2de145a59808)

![SSH command reference](https://github.com/user-attachments/assets/0ad46515-37b1-4835-acbd-828e971734ba)

Once connected, list the files:

```bash
ls
```

You should see output similar to:

![Files on the new instance](https://github.com/user-attachments/assets/27926b24-25e7-4f8e-b578-64a58ffc01c4)

## 8. Check Services and Start the App

Check the Node.js version and nginx status:

```bash
node -v
systemctl status nginx
```

Press `q` to exit the status view if needed.

Navigate to the app directory:

```bash
cd repo
ls
cd app
ls
```

Start the app:

```bash
pm2 start index.js --name tic
```

Open the new instance's public IP address in your browser to view the Tic Tac Toe app.
<img width="1292" height="702" alt="image" src="https://github.com/user-attachments/assets/54756bef-df4a-45f6-b5ef-5183245b6716" />

### Why is this useful?

Imagine a company has a website running on one server, and suddenly thousands of people start visiting.

The company may need additional servers.

Without an image, someone would have to install and configure everything on every new server.

With an image, the company can create new servers using a prepared starting point.

**Think of an AMI as a template of a furnished house.** Instead of buying an empty house and arranging the furniture again, you create another house with the same furniture already inside.

**Important:** An AMI copies the machine's disk setup, not its live running memory. So some programs may still need to be started when the new server boots.
