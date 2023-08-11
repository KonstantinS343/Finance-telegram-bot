import smtplib

from os.path import basename, dirname
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from celery_app import celery


def email_template(username: str, user_email: str):
    msg = MIMEMultipart()
    msg['Subject'] = 'Отчет'
    msg['From'] = SMTP_USER
    msg['To'] = user_email

    file = f'{dirname(__file__)}/reports/{username}_report.xlsx'

    with open(file, "rb") as f:
        part = MIMEApplication(
            f.read(),
            Name=basename(file)
        )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(file)
        msg.attach(part)
    return msg


@celery.task
def email_report(username: str, user_email: str):
    email = email_template(username=username, user_email=user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as email_server:
        email_server.login(SMTP_USER, SMTP_PASSWORD)
        email_server.send_message(email)
