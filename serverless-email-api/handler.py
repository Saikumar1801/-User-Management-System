# handler.py

import json
import os
import boto3
from botocore.exceptions import ClientError

# --- Setup ---
# When deployed, AWS provides credentials. Locally, boto3 might search for them.
# For local testing, we can provide dummy credentials so boto3 doesn't error out
# when we just want to test the logic before the AWS call.
# The 'serverless-offline' plugin often handles this, but this is a robust way.
session = boto3.Session(
    aws_access_key_id="mock",
    aws_secret_access_key="mock",
    region_name="us-east-1"
)
ses_client = session.client("ses")

# Get the sender email from the environment variables we set in serverless.yml
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")


def send_email(event, context):
    """
    This function is triggered by an API Gateway POST request.
    It parses the request body, validates it, and attempts to send an email.
    """
    print(f"Received event: {event}") # Good for debugging

    # --- 1. Input Validation and Error Handling ---
    try:
        # The body of the request comes in as a JSON string, so we need to parse it.
        body = json.loads(event.get("body", "{}"))
    except (json.JSONDecodeError, TypeError):
        print("ERROR: Invalid JSON in request body.")
        return {
            "statusCode": 400,  # Bad Request
            "body": json.dumps({"error": "Invalid JSON format in request body."})
        }

    receiver_email = body.get("receiver_email")
    subject = body.get("subject")
    body_text = body.get("body_text")

    # Check if all required fields are present
    if not all([receiver_email, subject, body_text]):
        print("ERROR: Missing required fields.")
        return {
            "statusCode": 400,  # Bad Request
            "body": json.dumps({"error": "Missing required fields: receiver_email, subject, and body_text are required."})
        }

    print(f"Attempting to send email from {SENDER_EMAIL} to {receiver_email}")

    # --- 2. The Core Logic: Sending the Email ---
    try:
        # This is the part that communicates with AWS SES.
        response = ses_client.send_email(
            Destination={"ToAddresses": [receiver_email]},
            Message={
                "Body": {"Text": {"Charset": "UTF-8", "Data": body_text}},
                "Subject": {"Charset": "UTF-8", "Data": subject},
            },
            Source=SENDER_EMAIL,
        )
        
        message_id = response.get("MessageId", "N/A_in_offline_mode")
        print(f"Email sent successfully! Message ID: {message_id}")

        # --- 3. Return a Success Response ---
        return {
            "statusCode": 200,  # OK
            "body": json.dumps({"message": "Email sent successfully!", "messageId": message_id})
        }

    # --- 4. Specific Error Handling for the AWS call ---
    except ClientError as e:
        # This will catch errors from boto3/AWS.
        # When running offline, this is where it will fail because we are not
        # connected to the real AWS. This is EXPECTED.
        error_message = e.response["Error"]["Message"]
        print(f"AWS CLIENT ERROR: {error_message}")
        return {
            "statusCode": 500,  # Internal Server Error
            "body": json.dumps({
                "error": "Failed to send email due to a service error.",
                "details": error_message
            })
        }