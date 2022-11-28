from django.db import models
from django.contrib.auth.models import User as DjangoUser


class PersonalData(models.Model):
    name = models.CharField('Имя')
    surname = models.CharField('Фамилия')
    # Пока что в стадии заглушки. Возможно расширить без ущерба для производства


# Create your models here.
class User(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    personal_data = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField('Проверенный пользователь', default=False)


class EventData(models.Model):
    data = models.TextField(null=True, blank=True)
    # Пока что в ставдии заглушки.


class Event(models.Model):
    name = models.CharField("Название мероприятия", default="Чемпионат по забиванию на дедлайны")
    data = models.OneToOneField(EventData, on_delete=models.CASCADE)


class StageData(models.Model):
    data = models.TextField(null=True, blank=True)
    # Пока что в стадии заглушки.


class Stage(models.Model):
    name = models.CharField("Название этапа", default="Я не знаю, что это такое")
    data = models.OneToOneField(StageData, on_delete=models.CASCADE)
    parent = models.ForeignKey(Event, on_delete=models.CASCADE)


class StageRelation(models.Model):
    stage_from = models.OneToOneField(Stage, on_delete=models.SET_NULL)
    stage_to = models.OneToOneField(Stage, on_delete=models.SET_NULL)
