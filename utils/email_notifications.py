from mailjet_rest import Client
from dotenv import load_dotenv
import os

load_dotenv()  # This loads variables from .env into the environment

def send_email(to_email, subject, body):
    """Send an email using Mailjet's API."""
    # Retrieve Mailjet API credentials from environment variables
    api_key = os.getenv('MAILJET_API_KEY')
    api_secret = os.getenv('MAILJET_API_SECRET')

    if not api_key or not api_secret:
        raise ValueError("Mailjet API credentials are not set in environment variables.")

    # Initialize Mailjet Client
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    # Define the email data
    data = {
        'Messages': [
            {
                "From": {
                    "Email": "kathanashjoshi@gmail.com",
                    "Name": "Kathan"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": "Dear Candidate"
                    }
                ],
                "Subject": subject,
                "TextPart": body,
                "HTMLPart": f"<p>{body}</p>"
            }
        ]
    }

    # Send the email
    result = mailjet.send.create(data=data)

    # Check and print the result
    if result.status_code == 200:
        print(f"Email sent to {to_email}")
    else:
        print(f"Failed to send email: {result.status_code}")
        print(result.json())
