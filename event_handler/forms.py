from django import forms

"""
    Форма для сбора информации мероприятия
"""

class Event(forms.Form):
    name = forms.CharField(label='Название мероприятия', required=True)
    privacy = forms.BooleanField(label='Приватное', required=True)
    thematic = forms.ChoiceField(label='Тематика', choices=['Олимпиада спортивная', 'Олимпиада ученическая'])
    date_start = forms.DateField(label='Дата начала', required=False)
    date_finsh = forms.DateField(label='Дата окончания', required=False)
    description = forms.TextInput()