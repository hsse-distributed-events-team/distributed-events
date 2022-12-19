from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from user_handler.regions.regions_dict import DATA_REGIONS, DATA_CITIES


class UserRegisterForm(UserCreationForm):  # User class
    email = forms.EmailField()
    region = forms.ChoiceField(choices=DATA_REGIONS)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'region']

