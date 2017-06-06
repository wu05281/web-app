from . import mail
from flask import render_template, current_app
from flask_mail import Message
from threading import Thread


def send_email(recipients, subject, template, **kwargs):
    msg = Message(subject=subject, recipients=[recipients])
    msg.body = subject
    msg.html = render_template(template + '.txt', **kwargs)
    thr = Thread(target=send_async_email, args=[current_app._get_current_object(), msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)