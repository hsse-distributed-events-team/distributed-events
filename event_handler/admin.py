from django.contrib import admin
from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'preview', 'status', 'time_start')

    # @admin.display(empty_value="А нету")
    # def parent_name(self, stage: Stage):
    #     return stage.parent.name


@admin.register(StageRelation)
class StageRelationAdmin(admin.ModelAdmin):
    list_display = ('stage_from', 'stage_to')


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')