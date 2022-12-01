from django.db import models
from user_handler.models import User
from enum import Enum


class Event(models.Model):
    name = models.CharField("Название мероприятия", default="Новое мероприятие", max_length=50)
    description = models.TextField(null=True, blank=True, max_length=500)

class Stage(models.Model):
    class StageStatus(models.IntegerChoices):
        WAITING = 0
        ACTIVE = 1
        ENDED = 2

    name = models.CharField("Название этапа", default="Новый этап", max_length=50)
    parent = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, max_length=500)
    preview = models.TextField(null=True, blank=True, max_length=100)
    users = models.ManyToManyField(User, through="Application")
    status = models.SmallIntegerField(null=True, default=StageStatus.WAITING, choices=StageStatus.choices)
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)


class StageRelation(models.Model):
    stage_from = models.OneToOneField(Stage, related_name="stage_from", on_delete=models.CASCADE)
    stage_to = models.OneToOneField(Stage, related_name="stage_to", on_delete=models.CASCADE)


class Venue(models.Model):
    name = models.CharField("Название", max_length=50)
    address = models.TextField("Адрес", max_length=500)


class Application(models.Model):
    class Status(models.IntegerChoices):
        AWAITED = 0
        ACCEPTED = 200
        REJECTED = 400
        BANNED = 404

    class Roles(models.IntegerChoices):
        PARTICIPANT = 0
        STAFF = 1
        ADMIN = 100

    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    role = models.SmallIntegerField("Роль", choices=Roles.choices, default=Roles.PARTICIPANT)
    last_update_time = models.DateTimeField()
    status = models.SmallIntegerField("Статус заявки", default=Status.AWAITED)
    result = models.TextField("Результат события", max_length=500)  # Пусть пока что результат будет длинной строкой
