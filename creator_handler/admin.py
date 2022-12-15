from django.contrib import admin
from .models import StageSettings

@admin.register(StageSettings)
class AdminStageSetting(admin.ModelAdmin):
    list_display = ("stage", )
