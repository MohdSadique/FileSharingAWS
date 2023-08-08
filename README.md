# FileSharingAWS
Developed a cloud-based file-sharing application using AWS services to facilitate secure file uploads and sharing with external users. Leveraged AWS Lambda, Amazon S3, Amazon DynamoDB, and Amazon SES to implement the application.

How To Setup:

IAM Role : 
To create an IAM role with permissions for S3, DynamoDB, and SES, follow these steps:

1.  Sign in to AWS Console: 
   Sign in to your AWS account using your credentials at https://aws.amazon.com/console/.

2.  Open IAM Service: 
   Once logged in, go to the AWS Management Console, and search for "IAM" in the search bar. Click on the "IAM" service to open it.

3.  Create a Role: 
   In the IAM dashboard, click on "Roles" in the left navigation pane, and then click on the "Create role" button.

4.  Select Type of Trusted Entity: 
   - On the "Create role" page, select the "AWS service" as the type of trusted entity.
   - From the "Choose the service that will use this role" dropdown, select "Lambda" (since we want to use this role for Lambda functions).

5.  Attach Permissions Policies: 
   - In the "Attach permissions policies" step, search for and select the following policies:
     - AmazonS3FullAccess: Provides full access to S3 buckets.
     - AmazonDynamoDBFullAccess: Provides full access to DynamoDB tables.
     - AmazonSESFullAccess: Provides full access to Simple Email Service (SES).
   - You can select these policies by checking the checkboxes next to them.


8.  Name and Create the Role: 
   - Give a name to your IAM role (e.g., "LambdaS3DynamoDBSESRole").
   - Click on the "Create role" button to create the IAM role.

Now you have created an IAM role with permissions for S3, DynamoDB, and SES. This role can be associated with your Lambda function, and the function will have the required permissions to interact with these AWS services.

Lambda Function:


1.  Sign in to AWS Console: 
   Sign in to your AWS account using your credentials at https://aws.amazon.com/console/.

2.  Open AWS Lambda Service: 
   Once logged in, go to the AWS Management Console, and search for "Lambda" in the search bar. Click on the "Lambda" service to open it.

3.  Create Function: 
   Click on the "Create function" button to create a new Lambda function.

4.  Choose Author from Scratch: 
   On the "Create function" page, select the "Author from scratch" option.

5.  Basic Function Configuration: 
   -  Function name:  Enter a name for your Lambda function.
   -  Runtime:  Choose the runtime for your function: Python
   -  Role:  Choose an existing role or create a new role that defines the permissions for your function. You can create a new role with basic Lambda execution permissions.

6.  Click "Create function": 
   After configuring the basic settings, click the "Create function" button at the bottom of the page.

7.  Edit the Lambda Function Code: 
   - In the "Function code" section, you can write your Lambda function code directly in the online code editor or upload a .zip file containing your function code.
   - For example, if you're using Python, you can write your Python code in the editor.

8.  Configure the Test Event: 
   - In the "Test events" section, you can configure test events to invoke your Lambda function for testing purposes.
   - You can create a new test event with sample JSON data to simulate the event that your function will receive when triggered.

9.  Test Your Lambda Function: 
   - Click on the "Test" button to manually test your Lambda function using the test event you configured.
   - Observe the output of your function in the "Execution result" section.

10.  Save Your Function: 
    - After testing your function, click on the "Save" button to save your Lambda function.

12.  Save and Deploy: 
    - After configuring triggers, click on the "Save" button to save your changes.
    - Click on the "Deploy" button to deploy your Lambda function to the selected triggers.


API Gateway:

To create an API in API Gateway that triggers a Lambda function and accepts `multipart/form-data` in a POST request using the proxy integration, follow these steps:

1.  Create the Lambda Function: 
   If you haven't created the Lambda function you want to trigger, create it first. Make sure the function is set up to handle `multipart/form-data` requests appropriately.

2.  Create the API: 
   - Go to the AWS Management Console, search for "API Gateway," and open the service.
   - Click on "Create API" and choose "REST API."

3.  Set up the API: 
   - Choose the "REST API" option and give your API a name.
   - Click on "Create API."

4.  Create a Resource and Method: 
   - In the API Gateway dashboard, click on "Create Resource."
   - Enter a resource name (e.g., "upload") and click on "Create Resource."
   - Under the new resource, click on "Create Method" and choose "POST" from the dropdown.

5.  Set up Integration with Lambda Function: 
   - Select "Lambda Function" as the integration type.
   - Choose the region where your Lambda function is deployed.
   - Type the name of your Lambda function in the "Lambda Function" field.
   - Click on "Save."

6.  Configure the Method: 
   - In the Method Execution pane, click on "Integration Request."
   - Under "HTTP Headers," click on "Add Header" and add the "Content-Type" header with the value "multipart/form-data."

7.  Enable Proxy Integration: 
   - In the "Integration Request" pane, select "Lambda Proxy Integration" under "Integration type."

8.  Deploy the API: 
   - Go back to the Resources list and select the "POST" method.
   - Click on "Deploy API" from the "Actions" dropdown.
   - Create a new deployment stage (e.g., "prod") and click on "Deploy."

9. Copy the API trigger link:
save it in the form uploadform.html and paste it in script submit event


Setup S3 Bucket

To set up an S3 bucket that will be triggered by a Lambda function and allow files stored in it to be accessed using a presigned URL by users outside of AWS, follow these steps:

1.  Create an S3 Bucket: 
   - Go to the AWS Management Console, search for "S3," and open the service.
   - Click on "Create bucket" and provide a unique name for your bucket.
   - Choose the region where you want to create the bucket.
   - Leave the default settings or customize them as per your requirements.
   -  make it public accessible in bucket permissions.
   - Click on "Create" to create the S3 bucket.


Create DynamoDB Table

1.  Go to the AWS Management Console: 

2.  Open DynamoDB Service: 
   - In the AWS Management Console, search for "DynamoDB" and open the DynamoDB service.

3.  Create a Table: 
   - In the DynamoDB dashboard, click on the "Create table" button.

4.  Enter Table Details: 
   - Enter a unique and meaningful name for your table in the "Table name" field.
   - Enter the attribute name for the primary key in the "Primary key" field. Choose the data type for the primary key. Since you want to use a datetime attribute, you can choose the "String" data type.


Setup SES

1.  Create an SES Account: 
   - Go to the AWS Management Console and navigate to the SES service.
   - Click on the "Get Started" button to start the SES setup process.

2.  Verify Domain or Email Addresses: 
   - Before sending emails, you need to verify your domain or email addresses.
   - If you want to send emails from your domain, you need to verify it. This involves adding DNS records to your domain's DNS configuration.
   - If you want to send emails from specific email addresses, you need to verify each email address.

4.  Verify Email Addresses: 
   - If you want to send emails from specific email addresses, follow the on-screen instructions to verify each email address.
   - SES will send a verification email to each address, and you need to click on the verification link in each email to complete the verification process.


Connect S3, DynamoDB and SES with Lambda Function:

Connect all this with lambda function with replacing parameters properly where ever necessary

Create EC2 Instance and host website

1.  Launch EC2 Instance: 
   - Go to the AWS Management Console and navigate to the EC2 service.
   - Click on the "Launch Instance" button.
   - Choose an Amazon Machine Image (AMI) of your choice Amazon Linux.
   - Select an instance type based on your requirements.
   - Configure instance details like the number of instances, network settings, etc.
   - Review your instance configuration and launch it.
   - Select an existing or create a new key pair to use for SSH access to the instance.

2.  Connect to the EC2 Instance using SSH: 
   - Once the instance is running, locate the public IP address or DNS name of the instance in the EC2 dashboard.
   - Open your terminal (for macOS/Linux) or use an SSH client 
   - Connect to the instance using the provided key pair:
     ```
     ssh -i /path/to/your/key.pem ec2-user@your-instance-public-ip
     ```

3.  Update and Install Required Packages: 
   - After connecting to the instance via SSH, update the package list and install Apache web server:
     ```
     sudo yum update -y
     sudo yum install httpd -y
     sudo service httpd start
     ```

4.  Upload Files to EC2 Instance: 
   - Use the `scp` command to securely copy your index.html and uploadform.htm files to the EC2 instance:
     ```
     scp -i /path/to/your/key.pem /path/to/index.html ec2-user@your-instance-public-ip:/tmp
     
      scp -i /path/to/your/key.pem /path/to/uploadform.htm ec2-user@your-instance-public-ip:/tmp
     ```

5.  Move Files to /var/www/html/: 
   - Move the uploaded files to the web server root directory and set appropriate permissions:
     ```
     sudo mv /tmp/index.html /var/www/html/
     sudo mv /tmp/uploadform.htm /var/www/html/
     ```

6.  Enable Public Access: 
   - By default, your EC2 instance should have a public IP address, allowing it to be publicly accessible.
   - If you need a domain name, you can associate an Elastic IP address with your instance and update DNS settings accordingly.

7.  Verify the Website: 
   - Open a web browser and navigate to your EC2 instance's public IP address or domain name (if set).
   - You should see your website hosted on the Apache web server.


Voila Your website  is up and running!
