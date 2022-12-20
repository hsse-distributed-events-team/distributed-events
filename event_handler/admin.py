from django.contrib import admin
from .models import Event, Stage, StageRelation, StageStaff, StageParticipants, Venue


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "parent", "preview", "status", "time_start")


@admin.register(StageRelation)
class StageRelationAdmin(admin.ModelAdmin):
    list_display = ("id", "stage_from", "stage_to")


@admin.register(StageParticipants)
class StageParticipantsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "stage", "role", "status")


@admin.register(StageStaff)
class StageStaffAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "stage", "role", "status")


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "parental_event", "contacts")
