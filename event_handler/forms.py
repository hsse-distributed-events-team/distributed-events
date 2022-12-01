from django import forms

"""
    Форма для сбора информации мероприятия
"""


class Event(forms.Form):
    name = forms.CharField(label='Название мероприятия', required=True)
    privacy = forms.BooleanField(label='Приватное', required=True)
    date = forms.DateField(label="Сроки проведения", )
