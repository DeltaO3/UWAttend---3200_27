import boto3
from botocore.exceptions import ClientError
import os

def send_email_ses(sender, recipient, subject, body_text, body_html):
    ses_client = boto3.client(
        'ses',
        region_name="ap-southeast-1",  
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),  # From IAM
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')# From IAM
    )

    CHARSET = "UTF-8"
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': [recipient],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': body_html,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': body_text,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': subject,
                },
            },
            Source=sender,
        )
        return response
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"Error sending email: {error_code} - {error_message}")
        if error_code == "SignatureDoesNotMatch":
            print("The request signature does not match. Check your AWS credentials and signing method.")
        elif error_code == "InvalidParameterValue":
            print("One of the parameters you provided is invalid. Check your input values.")
    

def get_welcome_email_details():
    subject = "Welcome to UWAttend"  
    
    body_text = "Hello,\nWelcome to UWAttend! This email contains important information."

    body_html = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }
            .container {
                width: 100%;
                padding: 20px;
            }
            .header {
                background-color: #4CAF50;
                color: white;
                padding: 10px 0;
                text-align: center;
            }
            .content {
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }
            .footer {
                margin-top: 20px;
                font-size: 12px;
                text-align: center;
                color: #888;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to UWAttend!</h1>
            </div>
            <div class="content">
                <h2>Hello!</h2>
                <p>Thank you for joining UWAttend. We're excited to have you on board!</p>
                <p>This email contains important information about your account.</p>
                <p>For assistance, please contact our support team.</p>
                <p>Visit our homepage: <a href="http://uwaengineeringprojects.com">UWAttend Homepage</a></p>
                <p>Best regards,<br>Your UWAttend Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 UWAttend. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return subject, body_text, body_html