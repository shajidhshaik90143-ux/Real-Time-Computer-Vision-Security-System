import os
import smtplib
from email.message import EmailMessage


def send_email_alert(
    subject,
    message
):

    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not all([
        sender,
        password,
        receiver
    ]):
        return False, "Email configuration missing"

    email = EmailMessage()

    email["Subject"] = subject
    email["From"] = sender
    email["To"] = receiver

    email.set_content(message)

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as server:

            server.login(
                sender,
                password
            )

            server.send_message(email)

        return True, "Email sent"

    except Exception as error:

        return False, str(error)