from django import forms
from .models import Participant

"""
    Форма для сбора информации мероприятия
"""


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'