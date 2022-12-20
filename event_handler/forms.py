from django import forms


class Event(forms.Form):
    """
        Форма для сбора информации мероприятия
    """
    name = forms.CharField(label='Название мероприятия', required=True)
    preview = forms.CharField(label='Превью', required=True)
    privacy = forms.BooleanField(label='Приватное', required=False)
    # thematic = forms.ChoiceField(label='Тематика', choices=['Олимпиада спортивная', 'Олимпиада ученическая'])
    date_start = forms.DateField(widget=forms.SelectDateWidget)
    date_finish = forms.DateField(widget=forms.SelectDateWidget)
    description = forms.CharField()
