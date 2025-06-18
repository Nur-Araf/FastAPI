from email.message import EmailMessage
import aiosmtplib
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve environment variables
SMTP_HOST = os.getenv("SMTP_HOST")
smtp_port_str = os.getenv("SMTP_PORT")

if smtp_port_str is None:
    raise ValueError("SMTP_PORT environment variable is not set")

SMTP_PORT = int(smtp_port_str)
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Your existing send_verification_email function
async def send_verification_email(to_email: str, token: str):
    verify_link = f"http://localhost:8000/api/v1/auth/verify-email?token={token}"
    message = EmailMessage()
    message["From"] = EMAIL_SENDER
    message["To"] = to_email
    message["Subject"] = "Verify Your Email"
    message.set_content(f"Click the link to verify your email: {verify_link}")
    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=EMAIL_SENDER,
            password=EMAIL_PASSWORD,
        )
        print(f"Verification email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send verification email to {to_email}: {str(e)}")
        raise
