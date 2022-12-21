from django import forms
from event_handler.models import StageStaff


class StaffForm(forms.ModelForm):
    """
    Класс **StaffForm**

    Форма для сбора информации о сотруднике


    """

    class Meta:
        model = StageStaff
        fields = '__all__'


class VenueForm(forms.Form):
    """
    Класс **StaffForm**

    Форма создания площадки

    :param name: Название мероприятия
    :param address: Адрес
    :param region: Регион
    :param participants_maximum: Максимальное число участников
    :param contacts: Контакты

    """

    name = forms.CharField(label='Название', required=True, max_length=50)
    address = forms.CharField(label='Адрес', required=True, max_length=500, widget=forms.Textarea)
    region = forms.IntegerField(label='Регион', required=False)
    participants_maximum = forms.IntegerField(label='Максимальное число участников', required=False, min_value=1)
    contacts = forms.CharField(label='Контакты', required=False, max_length=100, widget=forms.Textarea)
