from django.db import models
from user_handler.models import User
from enum import Enum


class StageStatus(Enum):
    WAITING = 0
    ACTIVE = 1
    ENDED = 2


class ApplicationStatus(Enum):
    AWAITED = 0
    ACCEPTED = 200
    REJECTED = 400
    BANNED = 404


class ApplicationRoles(Enum):
    PARTICIPANT = 0
    STAFF = 1
    ADMIN = 100


class Event(models.Model):
    name = models.CharField("Название мероприятия", default="Новое мероприятие", max_length=50)
    description = models.TextField(null=True, blank=True, max_length=500)
    users = models.ManyToManyField(User, through="Application")


class Stage(models.Model):
    name = models.CharField("Название этапа", default="Новый этап", max_length=50)
    parent = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, max_length=500)
    preview = models.TextField(null=True, blank=True, max_length=100)

    status = models.SmallIntegerField(null=True, default=StageStatus.WAITING)
    time_start = models.DateTimeField(null=True, blank=True)
    time_end = models.DateTimeField(null=True, blank=True)


class StageRelation(models.Model):
    stage_from = models.OneToOneField(Stage, related_name="stage_from", on_delete=models.CASCADE)
    stage_to = models.OneToOneField(Stage, related_name="stage_to", on_delete=models.CASCADE)


class Venue(models.Model):
    name = models.CharField("Название", max_length=50)
    address = models.TextField("Адрес", max_length=500)


class Application(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
    role = models.SmallIntegerField("Роль пользователя в мероприятии", default=ApplicationRoles.PARTICIPANT)
    last_update_time = models.DateTimeField()
    status = models.SmallIntegerField("Код статуса заявки", default=ApplicationStatus.AWAITED)
    result = models.TextField("Результат события", max_length=500)  # Пусть пока что результат будет длинной строкой
