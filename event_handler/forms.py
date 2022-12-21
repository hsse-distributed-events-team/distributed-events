from django import forms

class Event(forms.Form):
    """
    Класс **Event**

    Форма для сбора информации мероприятия

    :param name: Название мероприятия
    :param preview: Превью
    :param privacy: Приватное
    :param date_start: Дата окончания
    :param date_finish: Дата начала
    :param description: Описание

    """
    name = forms.CharField(label='Название мероприятия', required=True)
    preview = forms.CharField(label='Превью', required=True)
    privacy = forms.BooleanField(label='Приватное', required=False)
    # thematic = forms.ChoiceField(label='Тематика', choices=['Олимпиада спортивная', 'Олимпиада ученическая'])
    date_start = forms.DateField(widget=forms.SelectDateWidget)
    date_finish = forms.DateField(widget=forms.SelectDateWidget)
    description = forms.CharField()

class RegistrateEventForm(forms.Form):
    """
    Класс **RegistrateEventForm**

    :param venue_id: id площадки

    """
    venue_id = forms.IntegerField(label='id площадки', required=False, min_value=1)