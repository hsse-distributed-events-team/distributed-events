from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User as Profile
from .models import PersonalData
from user_handler.regions.regions_dict import DATA_REGIONS, DATA_CITIES


class UserRegisterForm(UserCreationForm):  # User class
    email = forms.EmailField()
    region = forms.ChoiceField(choices=DATA_REGIONS)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'region']


class UserUpdateForm(ModelForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=20, required=False)
    surname = forms.CharField(max_length=20, required=False)
    region = forms.ChoiceField(choices=DATA_REGIONS, required=False)

    class Meta:
        model = User
        fields = ['email', 'name', 'surname', 'region']
