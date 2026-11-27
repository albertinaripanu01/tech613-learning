# AWS CLI, Amazon S3, and Python Boto3 on Ubuntu

This guide shows how to install the AWS CLI on an Ubuntu x64 EC2 instance, authenticate it, manage an S3 bucket, and prepare Python Boto3.

## Install AWS CLI on an Ubuntu x64 VM

### 1. Connect to the instance

SSH into the new EC2 instance:

### 2. Update Ubuntu packages

```bash
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
```

`apt-get update` refreshes the list of available packages. `apt-get upgrade -y` installs available upgrades without asking for confirmation.

### 3. Install `unzip`

```bash
sudo apt install -y unzip
```

The AWS CLI download is a ZIP archive, so Ubuntu needs `unzip` to extract it.

### 4. Download AWS CLI version 2

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

This downloads the AWS CLI installer for 64-bit Linux and saves it as `awscliv2.zip`.

### 5. Extract the installer

```bash
unzip awscliv2.zip
```

This creates an `aws` directory containing the installer.

### 6. Install the AWS CLI

```bash
sudo ./aws/install
```

This installs the `aws` command so it can be run from any directory.

### 7. Verify the installation

```bash
aws --version
```

This prints the installed AWS CLI version.

## Configure the AWS CLI

### 1. Configure credentials

```bash
aws configure
```

Enter the following when prompted:

| Prompt | Value |
| --- | --- |
| AWS Access Key ID | Your IAM access key ID |
| AWS Secret Access Key | Your IAM secret access key |
| Default region name | `eu-west-1` |
| Default output format | `json` |

The command stores the credentials in `~/.aws/credentials` and the default settings in `~/.aws/config`.

### 2. Verify the configuration

```bash
aws s3 ls
```

This lists all S3 buckets that your IAM identity can access. It also confirms that the AWS CLI can authenticate successfully.

## Create and inspect an S3 bucket

### Create a bucket

```bash
aws s3 mb s3://tech613-albertina-first-bucket
```

`mb` means **make bucket**. Bucket names must be globally unique across AWS.

### List every available bucket

```bash
aws s3 ls
```

### List the files in one bucket

```bash
aws s3 ls s3://tech613-albertina-first-bucket
```

This lists objects in the named bucket. If the bucket is empty, the command succeeds but displays no files. If the bucket does not exist, AWS returns a `NoSuchBucket` error.

## Upload a file from Ubuntu to S3

### Create a test file

```bash
echo This is the first line in a test file > test.txt
```

The `>` symbol writes the text into a new file named `test.txt`.

### Confirm that the file exists

```bash
ls
```

### Upload the file

```bash
aws s3 cp test.txt s3://tech613-albertina-first-bucket
```

`cp` copies the local file into the S3 bucket.

### List files in the bucket

```bash
aws s3 ls s3://tech613-albertina-first-bucket
```

## Download files from S3

### Create and enter a download directory

```bash
mkdir downloads
cd downloads
```

### Download all files from the bucket

```bash
aws s3 sync s3://tech613-albertina-first-bucket .
```

`sync` downloads bucket objects into the current directory. The dot (`.`) means the current directory, which is `downloads` in this example.

### Confirm the downloaded files

```bash
ls -al
```

## Delete files from S3

### Delete one file

```bash
aws s3 rm s3://<bucket-name>/<file-name>
```

Example:

```bash
aws s3 rm s3://tech613-albertina-first-bucket/test.txt
```

### Delete all files

```bash
aws s3 rm s3://tech613-albertina-first-bucket --recursive
```

> **Warning:** `--recursive` deletes every object in the bucket.

## Delete the S3 bucket

```bash
aws s3 rb s3://tech613-albertina-first-bucket --force
```

`rb` means **remove bucket**. `--force` deletes the bucket and all objects still inside it.

> **Warning:** This action permanently deletes the bucket contents.

## Use Python Boto3 with S3

### Installation requirements

1. Python 3.10 or later:

   ```bash
   python3 --version
   ```

2. Install `venv` and `pip` if they are missing:

   ```bash
   sudo apt install -y python3-venv python3-pip
   ```

3. Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

   A virtual environment keeps project Python packages separate from Ubuntu's system Python packages.

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

   When active, the command prompt usually starts with `(venv)`.

### Install Boto3

```bash
pip3 install boto3
```

`pip3` installs the AWS SDK for Python into the active Python environment.

### Confirm the Boto3 version

```bash
python3 -c "import boto3; print(boto3.__version__)"
```

This imports Boto3 and prints its installed version. Boto3 automatically uses the credentials configured by `aws configure`.

<img width="745" height="48" alt="image" src="https://github.com/user-attachments/assets/7615754c-7f53-4b4b-b1dc-df51440b2f39" />
