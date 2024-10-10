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
    
    if type == 'welcome':
        recipient_encoded = urllib.parse.quote(recipient)
        subject, body_text, body_html = get_welcome_email_details(recipient_encoded)
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
    
    body_text = f"Hello,\nWelcome to UWAttend! Please create your account by visiting the link below:\n\n{link}"

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
                background-color: #A9A9FF;
                color: white;
                padding: 10px 0;
                text-align: center;
            }}
            .content {{
                background-color: white;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
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
                <p>Thank you for joining UWAttend!</p>
                <p>In order to create your account, please click the link: <a href="{link}">Create Account</a></p>
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

