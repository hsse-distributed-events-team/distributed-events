from django import forms
from event_handler.models import StageStaff

"""
    Форма для сбора информации мероприятия
"""


class StaffForm(forms.ModelForm):
    class Meta:
        model = StageStaff
        fields = '__all__'