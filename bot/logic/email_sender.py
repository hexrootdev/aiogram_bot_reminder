import asyncio

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from aiosmtplib import SMTP

from email_validator import validate_email, EmailNotValidError

from os import getenv
from dotenv import load_dotenv

load_dotenv()
mailer = getenv("MAILER")
password = getenv("EMAIL_APP_PASS")

async def send_email(to: str, content: str):  

    html_body = f"""
    <html>
        <body>
            {content}
        </body>
    </html>
    """

    msg = MIMEMultipart('alternative')
    msg["From"] = mailer
    msg["To"] = to
    msg["Subject"] = "Новое напоминание!"
    msg.attach(MIMEText(html_body, 'html'))
    
    client = SMTP(
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=mailer,
        password=password
        )
    async with client:
        await client.send_message(msg)

def get_validated_email(email):
    try:
        valid = validate_email(email, check_deliverability=True)
        return valid.email
    except EmailNotValidError:
        return False           


    
    
