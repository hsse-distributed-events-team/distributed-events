from django.core.mail import send_mail
from django.forms.widgets import Textarea
from django.forms.widgets import TextInput

from user_handler.models import User

def send_message(users, text: str, subject: str = "Уведомление"):
    us: User
    for us in users:
        send_mail(
            str(subject),
            str(text),
            'distrib.events@gmail.com',
            [us.user.email_user()],
        )