import boto3
import json
import os
from botocore.exceptions import ClientError
from datetime import datetime
import base64
import email

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object."""
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print("Error generating presigned URL: ", e)
        return None
    return response

def send_email(sender_email, recipient_emails, subject, body):
    """Send an email using AWS SES."""
    ses_client = boto3.client('ses', region_name='eu-north-1')  # Replace with your desired AWS region
    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': recipient_emails
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
    except ClientError as e:
        print("Error sending email: ", e)
        return False
    return True

def add_file_info_to_dynamodb(filename, datetime_str):
    """Add file information to DynamoDB."""
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('YOUR_DYNAMODB_TABLE_NAME')  # Replace with your DynamoDB table name

    try:
        response = table.put_item(
            Item={
                'filename': filename,
                'datetime': datetime_str
            }
        )
    except ClientError as e:
        print("Error adding file info to DynamoDB: ", e)
        return False
    return True

def lambda_handler(event, context):
    # Replace these values with your own
    sender_email = "sadik103.ss@gmail.com"
    s3_bucket = "uploadfilestorage"
    expiration_time = 3600  # Presigned URL expiration time in seconds
    # print("event:", event)
    # Get the uploaded file and email addresses from the API Gateway event
    
    # decoding form-data into bytes
    post_data = base64.b64decode(event["body"])
    # fetching content-type
    content_type = event["headers"]["content-type"]
    # concate Content-Type: with content_type from event
    ct = "Content-Type: " + content_type + "\n"
    # parsing message from bytes
    msg = email.message_from_bytes(ct.encode() + post_data)
    # checking if the message is multipart
    print("Multipart check : ", msg.is_multipart())
    print("1")
    dynamodb = boto3.resource('dynamodb')
    print("2")

    # if message is multipart
    if msg.is_multipart():
        multipart_content = {}
        # retrieving form-data
        for part in msg.get_payload():
            # checking if filename exist as a part of content-disposition header
            if part.get_filename():
                # fetching the filename
                file_name = part.get_filename()
                print("FileName : ", file_name)
            multipart_content[
                part.get_param("name", header="content-disposition")
            ] = part.get_payload(decode=True)
        
        # print("multipart_content :", multipart_content.keys())
        # u uploading file to S3
        s3 = boto3.client("s3")
        s3_upload = s3.put_object(Bucket=s3_bucket, Key=file_name, Body=multipart_content["file"])

        # Generate the presigned URL for the uploaded file
        presigned_url = generate_presigned_url(s3_bucket, file_name, expiration_time)
        if not presigned_url:
            return {
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'statusCode': 500,
                'body': 'Failed to generate presigned URL.'
            }
        
        # Send the email with the presigned URL to the provided email addresses
        subject = "Shared File Link"
        body = f"Here is the link to the shared file: {presigned_url}"
        
        emails = multipart_content["emails"]
        emails = json.loads(emails.decode('utf-8'))
        emails = list(filter(None,emails))

        if not send_email(sender_email,emails , subject, body):
            return {
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'statusCode': 500,
                'body': 'Failed to send the email.'
            }

        # Add file info to DynamoDB
        now = datetime.now()
        datetime_str = now.strftime("%Y-%m-%d %H:%M:%S")
        
        table = dynamodb.Table('UploadFilesRecord')  # Replace with your DynamoDB table name

        print("3")

        item = {
            'datetime': datetime_str,
            'filename': file_name,
            'presigned_url': presigned_url,
            'emails': emails
        }
        print(    'datetime', type(datetime_str))
        print(    'filename', type(file_name))
        print(    'presigned_url', type(presigned_url))
        print(    'emails', type(emails))
        

        try:
            response = table.put_item(Item=item)
            print("Response :", response)
        except ClientError as e:
            print("Error adding file info to DynamoDB: ", e)
            return {
                "headers": {
                    "Access-Control-Allow-Headers" : "Content-Type",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
                },
                'statusCode': 500,
                'body': 'Failed to add file info to DynamoDB.'
            }


        # on upload success
        return {
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
            "statusCode": 200,
            "body": json.dumps("File uploaded successfully!")
            }
    
 

    return {
            "headers": {
                "Access-Control-Allow-Headers" : "Content-Type",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
            },
        'statusCode': 500,
        'body': 'Upload Failed!'
    }
