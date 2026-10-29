# Launch Template and Auto Scaling Group Setup

## 1. Create a Launch Template

Configure the launch template with the following details:

- **Name:** `tech613-albertina-app-lt`
- **Version description:** `V1 for ASG`
- **Instance type:** `t3.micro`
- **Key pair name:** `tech613-albertina-aws-key`

![Launch template configuration](https://github.com/user-attachments/assets/787b0651-3124-4ea0-a75e-7bb28449a914)

![Instance type and key pair configuration](https://github.com/user-attachments/assets/f34d662e-272d-4572-8c97-f83caff51412)

### User Data

Add the following script to the **User data** field:

```bash
#!/bin/bash

sleep 2
cd /home/ubuntu/repo/app

pm2 start index.js --name tic
```

### Test the Launch Template

1. Create the launch template.
2. On the confirmation page, click the launch template ID.
3. Select **Actions → Launch instance from template**.
4. Review the instance configuration, then click **Launch instance**.
5. Open the instance summary and copy its **Public IPv4 address**.
6. Open the address in your browser and verify that the Tic Tac Toe app runs.
7. Once verified, terminate the test instance.

## 2. Create an Auto Scaling Group

Go to **EC2 → Auto Scaling groups → Create Auto Scaling group**.

### Choose a Launch Template

- **Auto Scaling group name:** `tech613-albertina-app-asg`
- **Launch template:** `tech613-albertina-app-lt`

Click **Next**.

### Choose Instance Launch Options

Select all three options shown below:

![Instance launch options](https://github.com/user-attachments/assets/0d00977f-770a-4933-8fa2-9d493bda8793)

Click **Next**.

### Integrate with Other Services

Configure the integration settings as shown:

![Service integration settings](https://github.com/user-attachments/assets/9c40cf11-aeec-4d9d-95af-e644cdd776c4)

- **Load balancer name:** `tech613-albertina-app-asg-lb`

![Load balancer configuration](https://github.com/user-attachments/assets/1100b8ed-8c72-4ab5-aa0a-90a4222f36eb)

![Additional load balancer settings](https://github.com/user-attachments/assets/040d6635-db12-466b-b05b-9903e0851bfc)

![Integration and health check settings](https://github.com/user-attachments/assets/38645373-7e83-4168-ac98-30b37da9cd1a)

### Configure Group Size and Scaling

Set the group capacity:

| Setting | Value |
| --- | --- |
| Desired capacity | `2` |
| Minimum capacity | `2` |
| Maximum capacity | `3` |

![Scaling configuration](https://github.com/user-attachments/assets/001e4ecb-ef45-4b4b-97d8-ed21304364c7)

- **Scaling policy name:** `Albertina ASG Target Tracking Policy`
- **Additional settings:** Select the monitoring checkbox.

Click **Next**.

### Add Notifications

Skip this optional step by clicking **Next**.

### Add Tags

Click **Add tag** and enter:

| Key | Value |
| --- | --- |
| `Name` | `tech613-Albertina-app-asg-hasc` |

Click **Next**.

### Review and Create

Review the configuration, then click **Create Auto Scaling group**.

## 3. Verify the App Deployment

1. Open the Auto Scaling group.
2. Select the **Instance management** tab.

![Auto Scaling group instance management](https://github.com/user-attachments/assets/87bc9d50-1a86-4ac5-a455-2fdb5bbc4449)

3. Click the first instance.

![Selected instance details](https://github.com/user-attachments/assets/8f4f8dd8-f4f9-404c-9fe7-56bfb66b62b0)

4. Copy its **Public IPv4 address**.
5. Open the address in your browser to verify that the Tic Tac Toe app is deployed.

## 4. Test Instance Replacement

1. Go to **EC2 → Instances**.

![EC2 instances](https://github.com/user-attachments/assets/5c843a32-ffb4-409f-8839-81a0c24328ad)

2. Select one instance named `tech613-Albertina-app-asg-hasc`.
3. Terminate the selected instance.
4. Return to **Auto Scaling groups** and open `tech613-albertina-app-asg`.
5. Refresh the page and check the activity and instance status.
6. Verify that the Auto Scaling group launches a replacement instance to maintain the desired capacity of `2`.

## 5. Clean Up Resources

After testing, delete the resources in this order:

1. **Auto Scaling group**
   - Go to **Auto Scaling groups**.
   - Select `tech613-albertina-app-asg`.
   - Select **Actions → Delete** and confirm.

2. **Load balancer**
   - Go to **Load balancers**.
   - Select `tech613-albertina-app-asg-lb`.
   - Select **Actions → Delete** and confirm.

3. **Target group**
   - Go to **Target groups**.
   - Select the target group created for this setup.
   - Select **Actions → Delete** and confirm.
