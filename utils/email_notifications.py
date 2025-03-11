import smtplib
from email.mime.text import MIMEText

def send_email(to_email, subject, body):
    """Send an email to the specified address."""
    # Replace with your email credentials (consider using environment variables for security)
    sender_email = "troxelllouisee@gmail.com"
    sender_password = "Kathan@1"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")