from email.message import EmailMessage
import aiosmtplib

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"  # Use App Password (not your Gmail password)

async def send_verification_email(to_email: str, token: str):
    verify_link = f"http://localhost:8000/api/v1/auth/verify-email?token={token}"

    message = EmailMessage()
    message["From"] = EMAIL_SENDER
    message["To"] = to_email
    message["Subject"] = "Verify Your Email"
    message.set_content(f"Click the link to verify your email: {verify_link}")

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=EMAIL_SENDER,
        password=EMAIL_PASSWORD,
    )
