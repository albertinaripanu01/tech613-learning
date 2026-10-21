# Deploy the Tic Tac Toe App on AWS

## 1. Create an AWS instance

Create an Ubuntu EC2 instance and allow inbound TCP traffic on ports **22**, **80**, and **3000**.

Use **Anywhere IPv4 (`0.0.0.0/0`)** as the source for your exercise.

Copy the instance’s **Public IPv4 address** from its details.

## 2. Open two Git Bash windows

- **Local window:** Connected to your own computer.
- **VM window:** Connected to your AWS instance.

In the VM window, connect using:

```bash
ssh -i ~/.ssh/tech613-albertina-aws-key.pem ubuntu@54.229.160.164
```

> Replace the key filename and IP address with your own key and instance’s public IPv4 address.

## 3. Upload the downloaded file

Focus on the **local Git Bash window**, without the VM connection.

The downloaded file is called `nodejs20-sparta-tictactoe-v1.zip` and is stored in your local Downloads folder.

Navigate to Downloads:

```bash
cd ~/Downloads
```

Copy the ZIP file to your instance:

```bash
scp -i ~/.ssh/tech613-albertina-aws-key.pem nodejs20-sparta-tictactoe-v1.zip ubuntu@54.229.160.164:/home/ubuntu/
```

> **Notes:**
> - Make sure the key filename matches the key stored in your local `~/.ssh` folder.
> - Replace `54.229.160.164` with the public IPv4 address of the instance you created.
> - Run this command on your local computer.

![Example SCP command](https://github.com/user-attachments/assets/8bc6e6dd-d091-420a-89aa-79d44c900a34)

After running the command, the output should look similar to this:

![Example upload output](https://github.com/user-attachments/assets/1085e726-5d73-447f-9b5e-d04edaba7a14)

## 4. Check the file on the VM

Switch to the **VM Git Bash window**.

Check whether the uploaded file is present:

```bash
ls
```

You should see `nodejs20-sparta-tictactoe-v1.zip`.

![File inside the VM](https://github.com/user-attachments/assets/60ee6488-0a50-4407-9cb7-dcdf55bde122)

## 5. Update the VM and extract the file

Run:

```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install unzip -y
sudo unzip nodejs20-sparta-tictactoe-v1.zip
```

> If your ZIP file has a different name, replace the filename in the final command.

![Extracting the ZIP file](https://github.com/user-attachments/assets/9038768c-2f5f-46ef-8335-20c4d20855f9)

## 6. Install Nginx and Node.js 20

Run these commands on the VM:

```bash
sudo apt install nginx -y
curl -sL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh
sudo apt install nodejs -y
```

## 7. Start the application

Navigate to the application folder and install its dependencies:

```bash
cd app
ls
npm install
npm start
```

> Keep the application running in this terminal while accessing it in Chrome.

## 8. Open the Tic Tac Toe app

Open this address in Chrome:

[http://54.229.160.164:3000](http://54.229.160.164:3000)

> Replace the IP address with your instance’s public IPv4 address.
>
> Use a **colon (`:`)** before port `3000`, not a dot.
>
> These steps access the app directly on port 3000. Installing Nginx alone does not configure forwarding from port 80.
