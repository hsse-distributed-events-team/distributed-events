from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'personal_data', 'is_verified')


@admin.register(PersonalData)
class PersonalDataAdmin(admin.ModelAdmin):
    list_display = ("name", "surname")
