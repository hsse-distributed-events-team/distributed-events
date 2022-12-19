from django import forms
from event_handler.models import StageStaff

"""
    Форма для сбора информации мероприятия
"""

#
# class StaffForm(forms.ModelForm):
#     class Meta:
#         model = StageStaff
#         fields = '__all__'

class VenueForm(forms.Form):
    """
        Форма создания площадки
    """

    name = forms.CharField(label='Название', required=True, max_length=50)
    address = forms.CharField(label='Адрес', required=True, max_length=500, widget=forms.Textarea)
    region = forms.IntegerField(label='Регион', required=False)
    participants_maximum = forms.IntegerField(label='Максимальное число участников', required=False, min_value=1)
    contacts = forms.CharField(label='Контакты', required=False, max_length=100, widget=forms.Textarea)
