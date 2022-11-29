from django import forms


class Event(forms.Form):
    name = forms.CharField(label='Название мероприятия', required=True)
    privacy = forms.BooleanField(label='Приватное', required=True)
    data = forms.DateField(label="Сроки проведения", )
