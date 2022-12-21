from django.core.mail import send_mail
from django.forms.widgets import Textarea
from django.forms.widgets import TextInput

from user_handler.models import User


def send_message(participants, text: str, subject: str = "Уведомление"):
    participant: User
    for participant in participants:
        send_mail(
            str(subject),
            str(text),
            'distrib.events@gmail.com',
            [participant.user.user.email],
        )
