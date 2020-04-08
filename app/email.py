from flask_mail import Message
from app import mail


def send_email(name, email, message):
    msg = Message('Email from Website', recipients=['booksthrubars@gmail.com'])
    msg.body = "You have received a new message from {} at {}: {}".format(name, email, message)
    mail.send(msg)
