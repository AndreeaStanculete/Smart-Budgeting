from django.contrib.auth.models import User

from email.message import EmailMessage
from smtplib import SMTP

from budgetingApp.utils.analyseData import buildEmailMessage, buildExportMessage
from budgetingApp.utils.excel import export_excel

from datetime import date

def sendEmailReport(user: User):
    messageBody = buildEmailMessage(user)
    attachment = export_excel(user)

    email = constructReportEmail(user.email, 'Your finances for the past month', messageBody, attachment)

    sendMailToServer(email)

def exportDataToEmail(user: User, month_year):
    messageBody = buildExportMessage(user, month_year)
    attachment = export_excel(user, month_year)

    email = constructReportEmail(user.email, "Your finances", messageBody, attachment)

    sendMailToServer(email)

def sendPasswordResetEmail(destination: str, unique_code: str):
    email = constructPasswordResetEmail(destination, "http://localhost:8000/account/password_reset/" + unique_code)

    sendMailToServer(email)

def constructPasswordResetEmail(destination: str, link: str) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = "Password reset"
    email['From'] = "EMAIL-HOST"
    email['To'] = [destination]
    email.set_content("Your one-time password reset link: " + link)

    print(email)

    return email

def constructReportEmail(destination: str, title: str, body: str, attachment) -> EmailMessage:
    email = EmailMessage()
    email['Subject'] = title
    email['From'] = "EMAIL-HOST"
    email['To'] = [destination]
    email.set_content(body, subtype='html')
    email.add_attachment(attachment.getvalue(), maintype='application/ms-excel', subtype='pdf', filename='Finances.xlsx')

    return email

def sendMailToServer(email: EmailMessage):
    EMAIL_ADDRESS = 'EMAIL-HOST'
    EMAIL_PASSWORD = 'EMAIL-PASSWORD'
    
    server = SMTP('smtp.gmail.com',587)
    server.starttls()

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.send_message(email)
    
    server.quit()