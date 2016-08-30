from flask_mail import Message, Mail

from app_config import config_class as config

mail = Mail()

def send_email(to, subject, template):
    message = Message(subject=subject,
                      recipients=[to],
                      html=template,
                      sender=config.MAIL_DEFAULT_SENDER
                      )
    mail.send(message)
