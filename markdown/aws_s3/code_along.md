# Week 5: Launch an EC2 Instance and Use Amazon S3

## 1. Launch the EC2 instance

In the AWS Console, launch a new EC2 instance with the following settings:

| Setting | Value |
| --- | --- |
| Instance name | `tech613-albertina-learn-s3` |
| AMI | Ubuntu Server 22.04 LTS |
| Instance type | `t3.micro` |
| Key pair | `albertina` |
| Security group | Select existing security group: `tech613-ramon-allow-ssh-http` |

Select **Launch instance**, then open the newly created instance.

## 2. Connect and update the server

Connect to the instance through Git Bash, then update Ubuntu:

```bash
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y
```

## 3. Set up the AWS CLI

Install the AWS CLI if it is not already installed, then confirm the installed version:

```bash
aws --version
```

Configure the CLI and enter your AWS access credentials when prompted:

```bash
aws configure
```

Use the following configuration values:

| Prompt | Value |
| --- | --- |
| Default region name | `eu-west-1` |
| Default output format | `json` |

## 4. Work with Amazon S3

List the S3 buckets available to your AWS account:

```bash
aws s3 ls
```

View help for S3 commands:

```bash
aws s3 help
```

Create an S3 bucket:

```bash
aws s3 mb s3://tech515-ramon-first-bucket
```

Create a local test file:

```bash
echo This is the first line in a test file > test.txt
```

Upload the file to the S3 bucket:

```bash
aws s3 cp test.txt s3://tech515-ramon-first-bucket
```

List the objects stored in the bucket:

```bash
aws s3 ls s3://tech515-ramon-first-bucket
```

> The final command lists files (objects) in the specified bucket. Use `aws s3 ls` without a bucket name to list all buckets.
> 
## 5. Additional S3 commands

| Task | Command |
| --- | --- |
| List buckets | `aws s3 ls` |
| Create a bucket | `aws s3 mb s3://tech515-ramon-first-bucket` |
| Upload a file | `aws s3 cp test.txt s3://tech515-ramon-first-bucket` |
| List files in a bucket | `aws s3 ls s3://tech515-ramon-first-bucket` |
| Download all bucket files to the current folder | `aws s3 sync s3://tech515-ramon-first-bucket .` |
| Download one file | `aws s3 cp s3://tech515-ramon-first-bucket/test.txt .` |

Remove every file in the bucket:

```bash
aws s3 rm s3://tech515-ramon-first-bucket --recursive
```

> **Danger:** This deletes all files in the bucket without prompting.

Remove the bucket and all files it contains:

```bash
aws s3 rb s3://tech515-ramon-first-bucket --force
```

> **Danger:** This deletes the bucket and every file in it without prompting.
