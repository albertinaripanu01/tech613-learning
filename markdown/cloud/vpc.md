
# Create VPC

Name: tech613-albertina-2tier-first-vpc  
IPv4 CIDR: 10.0.0.0/16

Press **Create VPC**.

## Subnets

Click **Create subnet**.

VPC ID: tech613-albertina-2tier-first-vpc  
Subnet name: tech613-albert-2tier-first-vpc-public-subnet

![Public subnet settings](https://github.com/user-attachments/assets/435a8390-3c4d-4699-8dce-7b8a2af75c5f)

2nd subnet name: tech613-albert-2tier-first-vpc-private-subnet

![Private subnet settings](https://github.com/user-attachments/assets/99f9a72a-ccd6-464b-9242-1708cf184b61)

Click **Create subnet**.

## Internet Gateway

Click **Create internet gateway**.

Name tag: tech613-albertina-2tier-first-vpc-ig

Create the new IG.

Immediately, it will show the green square confirming the creation and offering the **Attach to VPC** button.

![Internet gateway confirmation](https://github.com/user-attachments/assets/70eb98ef-8b0f-4727-88f7-d89d9ceb1ab0)

Select VPC **tech613-albertina-2tier-first-vpc**, and done.

## Route Tables

Name: tech613-albertina-2tier-first-vpc-public-rt  
VPC: tech613-albertina-2tier-first-vpc

Click **Create route table**.

Once created, go to the **Subnet associations** tab.

![Subnet associations](https://github.com/user-attachments/assets/09d5b47e-9b7b-48d0-87ad-79a969eaafe1)

Click **Edit subnet associations**.

Click the public one, then **Save associations**.

Once back, go to the **Actions** button, then click **Edit routes**.

![Edit routes](https://github.com/user-attachments/assets/7b0dd728-45b7-4aed-ada8-39eaa3a5fa48)

These are the settings:

![Route settings](https://github.com/user-attachments/assets/4a552008-d11e-42e7-a62a-8de5da19d2e6)

Click **Update route**.

## Launch the Database Instance

Go back to **EC2 → AMIs**, and remember the image:

tech603-ramon-ttt-test-db-ready-to-run

Now go to **Launch instances**.

Name: tech613-albertina-2tier-first-vpc-ttt-db-vm

![Database instance settings](https://github.com/user-attachments/assets/e39c9629-617e-416d-8eac-fe02fbfb5154)

![Database instance settings](https://github.com/user-attachments/assets/6810f699-6f2c-4588-b89f-ea627b9d070c)

Click **Edit** next to **Network settings** and change the VPC to your own.

![Database VPC settings](https://github.com/user-attachments/assets/051950aa-8f2a-47bc-984e-7cd1239911d9)

Create your security group.

Name: tech613-albertina-2tier-first-vpc-ttt-db-allow-ssh-mongodb

![Database security group](https://github.com/user-attachments/assets/69c19490-abd7-4e75-93b9-870ab0625aee)

![Database security group rules](https://github.com/user-attachments/assets/8e50f884-ee5b-42ca-8eea-7cec25c3fb37)

Click **Launch instance**.

## Launch the App Instance

Go to **AMIs**.

Select **tech603-ramon-ttt-test-app-ready-to-run**, then click **Launch instance from AMI**.

Name: tec613-albertina-2tier-first-vpc-ttt-app-vm

![App instance settings](https://github.com/user-attachments/assets/6907824d-69f9-4464-acc2-288a7c7b56ed)
<img width="832" height="342" alt="image" src="https://github.com/user-attachments/assets/14a658bc-4cd4-4594-9e1a-ac38832fdbc9" />


Security group name — required:

tech613-albertina-2tier-first-vpc-ttt-db-allow-ssh-http

![App security group](https://github.com/user-attachments/assets/00f13bca-0301-4356-a5fa-ef1d9c00a827)

Add in **User data**.

Make sure you replace the IPv4 address with the public IP address of **tech613-albertina-2tier-first-vpc-ttt-db-vm**.

```bash
#!/bin/bash

cd repo/app

export MONGODB_URI=mongodb://10.0.3.135:27017/tictactoe

pm2 start index.js --name tic
```

Click **Launch instance**.

      
2:17
