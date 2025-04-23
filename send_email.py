import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_SERVER

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject.replace('\n', '').replace('\r', '')

    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to, msg.as_string())
