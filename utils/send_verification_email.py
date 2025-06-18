import asyncio
from email.message import EmailMessage
import aiosmtplib
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve SMTP settings
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

async def test_email():
    message = EmailMessage()
    message["From"] = EMAIL_SENDER
    message["To"] = "cocshishir72@gmail.com"  # Replace with a real recipient email
    message["Subject"] = "Test Email"
    message.set_content("This is a test email.")

    try:
        await aiosmtplib.send(
            message,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            start_tls=True,
            username=EMAIL_SENDER,
            password=EMAIL_PASSWORD,
        )
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_email())