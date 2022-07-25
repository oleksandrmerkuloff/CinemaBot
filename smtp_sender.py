# not working because google closed accessing with email and pass
import smtplib
import ssl
from email.message import EmailMessage

def send_email(message, full_name):
    
    sender = "test@gmail.com"
    _password = 'apllication password'
    reciver = 'test@gmail.com'
    
    subject = f'Резюме на роботу від {full_name}'

    letter = EmailMessage()
    letter['From'] = sender
    letter['To'] =  reciver
    letter['Subject'] = subject
    
    with open(message, 'rb') as f:
        file_data = f.read()
        file_name = f.name

    letter.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file_name)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp_conn:
        smtp_conn.login(sender, _password)
        smtp_conn.send_message(letter)

if __name__ == '__main__':
    send_email(r'H:\resume\resume.pdf')