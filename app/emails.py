import boto3
from botocore.exceptions import ClientError
import os
import urllib.parse

def valid_email(email):
    # Check if the email contains one “@” symbol
    if email.count('@') != 1:
        return False

    # Split the email into local part and domain part
    local_part, domain_part = email.split('@')

    # Check if both the local part and domain part are not empty
    if len(local_part) == 0 or len(domain_part) == 0:
        return False

    # Check if the domain part contains a dot (.)
    if domain_part.find('.') == -1:
        return False

    return True

def send_email_ses(sender, recipient, type):

    sender = sender
    recipient = recipient

    if not valid_email(recipient):
        return False
    if not valid_email(sender):
        return False
    
    recipient_encoded = urllib.parse.quote(recipient)
    
    if type == 'welcome':
        subject, body_text, body_html = get_welcome_email_details(recipient_encoded)

    elif type == 'forgot_password':
        subject, body_text, body_html = get_forgot_password_email_details(recipient_encoded)
    else: 
        return False
    
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
        print(response)
        return True
    except ClientError as e:
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        print(f"Error sending email: {error_code} - {error_message}")
        if error_code == "SignatureDoesNotMatch":
            print("The request signature does not match. Check your AWS credentials and signing method.")
        elif error_code == "InvalidParameterValue":
            print("One of the parameters you provided is invalid. Check your input values.")
        return False
    

def get_welcome_email_details(recipient_encoded):
    link = f"https://uwaengineeringprojects.com/create_account?email={recipient_encoded}"

    subject = "Welcome to UWAttend"  
    
    # Plain text version of the email body for email clients that don't support HTML
    body_text = (
        f"Hello,\n"
        f"Welcome to UWAttend! Please create your account by visiting the link below:\n\n"
        f"{link}\n"
    )

    # HTML version of the email body for email clients that support HTML
    body_html = """
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
            }}
            .header {{
                background-color: #68bbe3;
                color: white;
                padding: 10px 0;
                text-align: center;
            }}
            .content {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #68bbe3;
                text-decoration: none;
                border-radius: 5px;
            }}
            .button:hover {{
                background-color: #3333FF;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                text-align: center;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to UWAttend!</h1>
            </div>
            <div class="content">
                <h2>Hello!</h2>
                <p>Thank you for joining UWAttend! To create your account, please click the button below:</p>
                <p><a href="{link}" class="button">Create Account</a></p>
                <p>Best regards,<br>Your UWAttend Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 UWAttend. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """.format(link=link)

    return subject, body_text, body_html

def get_forgot_password_email_details(recipient_encoded):
    link = f"https://uwaengineeringprojects.com/reset_password?email={recipient_encoded}"

    subject = "Password Reset Request"

    # Plain text version of the email body for email clients that don't support HTML
    body_text = (
        f"Hello,\n"
        f"We received a request to reset your password. To proceed, please click the link below:\n\n"
        f"{link}\n"
        f"If you did not request a password reset, please ignore this email.\n"
    )

    body_html = """
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 100%;
                padding: 20px;
            }}
            .header {{
                background-color: #68bbe3;
                color: white;
                padding: 10px 0;
                text-align: center;
            }}
            .content {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #68bbe3;
                text-decoration: none;
                border-radius: 5px;
            }}
            .button:hover {{
                background-color: #3333FF;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                text-align: center;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>UWAttend Password Reset</h1>
            </div>
            <div class="content">
                <h2>Hello!</h2>
                <p>We received a request to reset your password. To proceed, please click the button below:</p>
                <p><a href="{link}" class="button">Reset Password</a></p>
                <p>If you did not request a password reset, please ignore this email.</p>
                <p>Best regards,<br>Your UWAttend Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 UWAttend. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """.format(link=link)

    return subject, body_text, body_html