import smtplib

from os.path import basename, dirname
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD
from celery_app import celery


def email_template(username: str, user_email: str):
    msg = MIMEMultipart()
    msg['Subject'] = 'Отчет'
    msg['From'] = SMTP_USER
    msg['To'] = user_email

    file = f'{dirname(__file__)}/reports/{username}_report.xlsx'
    income_diagram = f'{dirname(__file__)}/diagrams/{username}_income_diagram.png'
    expenditure_diagram = f'{dirname(__file__)}/diagrams/{username}_expenditure_diagram.png'

    with open(file, "rb") as f:
        part = MIMEApplication(f.read(), name=basename(file))
        msg.attach(part)

    with open(income_diagram, 'rb') as image_file:
        image = MIMEImage(image_file.read(), name=f'{username}_income_diagram.png')
        msg.attach(image)

    with open(expenditure_diagram, 'rb') as image_file:
        image = MIMEImage(image_file.read(), name=f'{username}_income_diagram.png')
        msg.attach(image)

    return msg


@celery.task
def email_report(username: str, user_email: str):
    email = email_template(username=username, user_email=user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as email_server:
        email_server.login(SMTP_USER, SMTP_PASSWORD)
        email_server.send_message(email)
