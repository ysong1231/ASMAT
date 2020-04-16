import os
import smtplib, ssl
from dotenv import load_dotenv

load_dotenv()
port = 465
smtp_server = "smtp.gmail.com"
sender_email = os.getenv('EMAIL_SENDER')
receiver_email = os.getenv('EMAIL_RECEIVER')
password = os.getenv('EMAIL_PASSWORD')

def send_email(message):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)